import requests
from .utils import format_fax_number

API_URL = "https://npiregistry.cms.hhs.gov/api/"

def get_provider_info(npi: str) -> dict:
    """Query CMS NPI Registry API for provider info."""
    params = {"number": npi, "version": "2.1"}
    try:
        data = requests.get(API_URL, params=params, timeout=30).json()
    except Exception:
        return {"# Fax": None, "NPI": npi, "Name": None, "NPI type": None, "Error": "API request failed"}

    if "Errors" in data and data["Errors"]:
        return {"# Fax": None, "NPI": npi, "Name": None, "NPI type": None,
                "Error": data["Errors"][0].get("description", "Unknown error")}

    if data.get("result_count", 0) == 0 or not data.get("results"):
        return {"# Fax": None, "NPI": npi, "Name": None, "NPI type": None, "Error": "EMPTY"}

    result = data["results"][0]
    basic = result.get("basic", {})
    enumeration_type = result.get("enumeration_type")

    if enumeration_type == "NPI-1":
        name = " ".join([p for p in [basic.get("first_name",""), basic.get("middle_name",""),
                                     basic.get("last_name",""), basic.get("credential","")] if p])
        NPI_type = "NPI-1 Individual"
    elif enumeration_type == "NPI-2":
        name = basic.get("organization_name", "")
        NPI_type = "NPI-2 Organization"
    else:
        name, NPI_type = None, None

    fax = None
    for addr in result.get("addresses", []):
        if addr.get("fax_number"):
            fax = format_fax_number(addr["fax_number"])
            break

    error_reason = None if fax else "Fax number not available"
    return {"# Fax": fax, "NPI": npi, "Name": name, "NPI type": NPI_type, "Error": error_reason}
