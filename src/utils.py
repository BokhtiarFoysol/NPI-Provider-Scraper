import re
import pandas as pd

def format_fax_number(number: str) -> str:
    """Format fax number into (XXX)XXX-XXXX if possible."""
    if number:
        digits = re.sub(r"\D", "", number)
        if len(digits) == 10:
            return f"({digits[0:3]}){digits[3:6]}-{digits[6:10]}"
    return number

def format_npi(value) -> str:
    """Normalize NPI values to integer strings, stripping .0 and blanks."""
    try:
        if pd.isna(value) or value is None or str(value).strip() == "":
            return ""
        return str(int(float(value)))
    except Exception:
        return str(value)
