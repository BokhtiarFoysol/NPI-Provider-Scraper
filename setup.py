from setuptools import setup, find_packages

setup(
    name="NPI-Provider-Scraper",
    version="0.1.0",
    description="Extract provider info from CMS NPI Registry API and scrape missing data",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "requests",
        "playwright"
    ],
    entry_points={
        "console_scripts": [
            "npi-provider-scraper=main:cli"
        ]
    },
)
