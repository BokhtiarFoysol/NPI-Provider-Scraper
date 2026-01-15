# NPI-Provider-Scraper
A Python CLI pipeline for batch processing National Provider Identifier (NPI) datasets. The tool performs data cleaning and deduplication, enriches records via the CMS NPI Registry API, and selectively scrapes provider view pages using Playwright to resolve empty or deactivated NPIs, producing structured CSV outputs with summary analytics

# Provider Info NPI Extractor

This project extracts provider information (fax, name, NPI type, error reasons) from the CMS NPI Registry API and supplements missing data by scraping the provider-view page using Playwright.


## Installation
Clone the repo and install dependencies:
```bash
git clone https://github.com/yourusername/provider-info-npi.git
cd provider-info-npi
pip install -r requirements.txt
playwright install chromium
playwright install-deps

