import json
from pathlib import Path

import requests


PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "helsinki"

BASE_URL = "https://www.hel.fi/palvelukarttaws/rest/v4"

ENDPOINTS = {
    "ontologyword": f"{BASE_URL}/ontologyword/",
    "ontologytree": f"{BASE_URL}/ontologytree/",
    "arealcity": f"{BASE_URL}/arealcity/",
    "unit": f"{BASE_URL}/unit/",
}


def download_data(name, url):
    """Download data from a Service Map API endpoint."""
    print(f"Downloading {name}...")

    response = requests.get(
        url,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    print(f"  Downloaded {len(data):,} records.")

    return data


def save_data(name, data):
    """Save downloaded data as a JSON file."""
    output_file = OUTPUT_DIR / f"{name}.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

    print(f"  Saved to: {output_file}")


def main():
    """Download and save all required Service Map data."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("Downloading Helsinki Service Map data...\n")

    for name, url in ENDPOINTS.items():
        data = download_data(name, url)
        save_data(name, data)

    print("\nDownload complete!")


if __name__ == "__main__":
    main()