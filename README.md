# NPI-Provider-Scraper
A Python CLI pipeline for batch processing National Provider Identifier (NPI) datasets. The tool performs data cleaning and deduplication, enriches records via the CMS NPI Registry API, and selectively scrapes provider view pages using Playwright to resolve empty or deactivated NPIs, producing structured CSV outputs with summary analytics
