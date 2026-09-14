import pandas as pd
from pathlib import Path


# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

BUSINESS_FILE = PROCESSED_DATA / "yelp_business_processed.csv"
REVIEW_FILE = PROCESSED_DATA / "yelp_reviews_processed.csv"


def check_business_ids():
    """Check that review business IDs exist in the business file."""

    print("Checking business IDs...")

    businesses = pd.read_csv(
        BUSINESS_FILE,
        usecols=["business_id"]
    )

    business_ids = set(businesses["business_id"])

    review_business_ids = set()
    missing_business_ids = set()

    for chunk in pd.read_csv(
        REVIEW_FILE,
        usecols=["business_id"],
        chunksize=100_000
    ):
        ids = set(chunk["business_id"])

        review_business_ids.update(ids)
        missing_business_ids.update(
            ids - business_ids
        )

    matching_ids = review_business_ids - missing_business_ids

    print(f"Unique business IDs in business file: {len(business_ids):,}")
    print(f"Unique business IDs in review file: {len(review_business_ids):,}")
    print(f"Matching business IDs: {len(matching_ids):,}")
    print(f"Business IDs in reviews but not business file: {len(missing_business_ids):,}")

    if len(missing_business_ids) == 0:
        print("✓ All review business IDs exist in the business file.")
    else:
        print("⚠ Some review business IDs are missing from the business file.")

    print()


def check_repeated_users():
    """Check whether users have multiple reviews."""

    print("Checking repeated user IDs...")

    user_review_counts = {}

    for chunk in pd.read_csv(
        REVIEW_FILE,
        usecols=["user_id"],
        chunksize=100_000
    ):
        counts = chunk["user_id"].value_counts()

        for user_id, count in counts.items():
            user_review_counts[user_id] = (
                user_review_counts.get(user_id, 0) + count
            )

    total_users = len(user_review_counts)

    users_with_multiple_reviews = sum(
        count > 1
        for count in user_review_counts.values()
    )

    maximum_reviews = max(user_review_counts.values())

    print(f"Unique users: {total_users:,}")
    print(
        f"Users with multiple reviews: "
        f"{users_with_multiple_reviews:,}"
    )
    print(
        f"Maximum reviews by one user: "
        f"{maximum_reviews:,}"
    )

    if users_with_multiple_reviews > 0:
        print("✓ Multiple reviews from the same user exist.")
    else:
        print("⚠ No users have multiple reviews.")

    print()


def main():
    check_business_ids()
    check_repeated_users()

    print("Relationship checks complete!")


if __name__ == "__main__":
    main()