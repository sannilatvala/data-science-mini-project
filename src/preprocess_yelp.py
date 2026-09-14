import tarfile
from pathlib import Path

import pandas as pd


# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

YELP_TAR = RAW_DATA / "yelp_dataset.tar"

BUSINESS_OUTPUT = PROCESSED_DATA / "yelp_business_processed.csv"
REVIEW_OUTPUT = PROCESSED_DATA / "yelp_reviews_processed.csv"


def create_output_directory():
    """Create the processed data directory."""
    PROCESSED_DATA.mkdir(parents=True, exist_ok=True)


def load_business_data(tar):
    """Load only the required business columns from the TAR file."""

    print("Loading business data...")

    member = tar.getmember(
        "yelp_academic_dataset_business.json"
    )

    with tar.extractfile(member) as file:
        businesses = pd.read_json(file, lines=True)

    businesses = businesses[
        ["business_id", "categories"]
    ]

    businesses = businesses.dropna(
        subset=["categories"]
    )

    print(f"Loaded {len(businesses):,} businesses.")

    return businesses


def save_business_data(businesses):
    """Save the processed business data."""

    businesses.to_csv(
        BUSINESS_OUTPUT,
        index=False
    )

    print(f"Business data saved to: {BUSINESS_OUTPUT}")


def process_review_data(tar, business_ids):
    """Process review data in chunks and keep only valid business IDs."""

    print("Loading review data...")

    member = tar.getmember(
        "yelp_academic_dataset_review.json"
    )

    total_reviews = 0
    kept_reviews = 0
    removed_reviews = 0
    first_chunk = True

    with tar.extractfile(member) as file:
        for chunk in pd.read_json(
            file,
            lines=True,
            chunksize=100_000
        ):
            chunk = chunk[
                ["user_id", "business_id", "stars"]
            ]

            total_reviews += len(chunk)

            # Keep only reviews for businesses
            # that exist in the processed business data.
            chunk = chunk[
                chunk["business_id"].isin(business_ids)
            ]

            kept_reviews += len(chunk)
            removed_reviews = total_reviews - kept_reviews

            chunk.to_csv(
                REVIEW_OUTPUT,
                mode="w" if first_chunk else "a",
                header=first_chunk,
                index=False
            )

            first_chunk = False

            print(
                f"Processed {total_reviews:,} reviews..."
            )

    print(f"Total reviews processed: {total_reviews:,}")
    print(f"Reviews kept: {kept_reviews:,}")
    print(f"Reviews removed: {removed_reviews:,}")
    print(f"Review data saved to: {REVIEW_OUTPUT}")


def preprocess_yelp():
    """Run the complete Yelp preprocessing pipeline."""

    create_output_directory()

    print("Opening Yelp dataset...\n")

    with tarfile.open(YELP_TAR, "r") as tar:
        businesses = load_business_data(tar)

        # Create a set of valid business IDs from the
        # processed business data.
        business_ids = set(businesses["business_id"])

        save_business_data(businesses)

        process_review_data(tar, business_ids)

    print("\nPreprocessing complete!")


if __name__ == "__main__":
    preprocess_yelp()