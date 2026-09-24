import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

BUSINESS_INPUT = PROCESSED_DATA / "yelp_business_processed.csv"
REVIEW_INPUT = PROCESSED_DATA / "yelp_reviews_processed.csv"
COMBINED_OUTPUT = PROCESSED_DATA / "combined.csv"


businesses = pd.read_csv(BUSINESS_INPUT)

reviews = pd.read_csv(REVIEW_INPUT)


combined = reviews.merge(
    businesses,
    on="business_id",
    how="left"
)


combined.to_csv(
    COMBINED_OUTPUT,
    index=False
)

print(f"Combined data saved to: {COMBINED_OUTPUT}")

print(combined.head())


user_preferences = combined.groupby("user_id")[
    ["business_id", "categories", "stars"]
].apply(lambda x: x.to_dict("records"))

print(user_preferences.head(10))
