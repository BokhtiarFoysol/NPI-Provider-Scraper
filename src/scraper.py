from playwright.async_api import async_playwright

async def scrape_npi(npi_number: str) -> str:
    """Scrape provider-view page for error messages when API returns empty results."""
    url = f"https://npiregistry.cms.hhs.gov/provider-view/{npi_number}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        try:
            locator = page.locator(".alert")
            error_msg = await locator.text_content(timeout=10000)
            if error_msg:
                if "deactivated" in error_msg.lower():
                    return "CMS deactivated this NPI"
                elif "no matching" in error_msg.lower():
                    return "No matching records found"
                else:
                    return error_msg
        except:
            return None
        finally:
            await browser.close()
