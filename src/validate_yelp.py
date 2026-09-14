import pandas as pd
from pathlib import Path


# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

BUSINESS_FILE = PROCESSED_DATA / "yelp_business_processed.csv"
REVIEW_FILE = PROCESSED_DATA / "yelp_reviews_processed.csv"


def check_business_data():
    """Check for missing or empty values in business data."""

    print("Checking business data...")

    businesses = pd.read_csv(BUSINESS_FILE)

    columns = ["business_id", "categories"]

    for column in columns:
        missing = businesses[column].isna().sum()
        empty = businesses[column].astype(str).str.strip().eq("").sum()

        print(f"{column}:")
        print(f"  Missing values: {missing:,}")
        print(f"  Empty values: {empty:,}")

    print(f"Total businesses: {len(businesses):,}\n")


def check_review_data():
    """Check for missing or empty values in review data."""

    print("Checking review data...")

    reviews = pd.read_csv(REVIEW_FILE)

    columns = ["user_id", "business_id", "stars"]

    for column in columns:
        missing = reviews[column].isna().sum()
        empty = reviews[column].astype(str).str.strip().eq("").sum()

        print(f"{column}:")
        print(f"  Missing values: {missing:,}")
        print(f"  Empty values: {empty:,}")

    print(f"Total reviews: {len(reviews):,}\n")


def validate_yelp():
    """Run all validation checks."""

    check_business_data()
    check_review_data()

    print("Validation complete!")


if __name__ == "__main__":
    validate_yelp()