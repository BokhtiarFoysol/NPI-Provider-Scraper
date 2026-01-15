import pandas as pd
import asyncio
import sys
from .api_utils import get_provider_info
from .scraper import scrape_npi
from .utils import format_npi

CHUNK_SIZE = 10
OUTPUT_FILE = "provider_info.csv"

async def process_file(input_file: str):
    # Load and clean NPI column
    header_df = pd.read_csv(input_file, nrows=0)
    cols_lower = {col.lower(): col for col in header_df.columns}
    if "npi" not in cols_lower:
        raise ValueError("CSV must contain a column named 'NPI' (any case variation).")

    actual_npi_col = cols_lower["npi"]
    df = pd.read_csv(input_file, usecols=[actual_npi_col])
    df.columns = ["npi"]
    df["npi"] = df["npi"].apply(format_npi)

    # Remove blanks and duplicates
    df = df[df["npi"].str.strip() != ""].drop_duplicates(subset=["npi"], keep="first")

    all_results = []
    for start in range(0, len(df), CHUNK_SIZE):
        chunk = df.iloc[start:start+CHUNK_SIZE]
        results = [get_provider_info(npi) for npi in chunk["npi"].astype(str).str.strip()]

        tasks = [scrape_npi(r["NPI"]) if r["Error"]=="EMPTY" else None for r in results]
        scrape_results = await asyncio.gather(*[t for t in tasks if t])

        scrape_iter = iter(scrape_results)
        for r in results:
            if r["Error"]=="EMPTY":
                r["Error"] = next(scrape_iter) or "Unknown empty result"

        all_results.extend(results)
        print(f"Processed rows {start}–{start+len(chunk)}")

    out_df = pd.DataFrame(all_results)
    out_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved provider info to {OUTPUT_FILE}")

def cli():
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <input_csv>")
        sys.exit(1)
    input_file = sys.argv[1]
    asyncio.run(process_file(input_file))

if __name__ == "__main__":
    cli()
