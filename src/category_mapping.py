import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
YELP_DATA = PROCESSED_DATA / "combined.csv"
OUTPUT_DATA = PROCESSED_DATA / "combined_with_categories.csv"


category_mapping = {
    "Museums": "museum",
    "Comedy Clubs": "theatre",
    "Performing Arts": "theatre",
    "Cinema": "cinema",
    "Bowling": "bowling",
    "Climbing": "climbing",
    "Hiking": "hiking",
    "Tennis": "tennis",
    "Swimming Pools": "swimming",
    "Swimming Lessons/Schools": "swimming",
    "Gyms": "fitness",
    "Martial Arts": "martial arts",
    "Skating Rinks": "ice skating",
    "Golf": "golf",
    "Mini Golf": "mini golf",
    "Disc Golf": "disc golf",
    "Art Museums": "art gallery",
    "Zoos": "zoo",
    "Dance Studios": "Dance"
}


def map_categories(categories):
    if pd.isna(categories):
        return None

    categories = [x.strip() for x in categories.split(",")]

    mapped = {
        category_mapping[x]
        for x in categories
        if x in category_mapping
    }

    return "; ".join(sorted(mapped)) if mapped else None


first_chunk = True

for chunk in pd.read_csv(YELP_DATA, chunksize=10000):

    chunk["helsinki_category"] = chunk["categories"].apply(map_categories)

    chunk.to_csv(
        OUTPUT_DATA,
        mode="w" if first_chunk else "a",
        header=first_chunk,
        index=False
    )

    first_chunk = False

print("Done!")
print(f"Saved to: {OUTPUT_DATA}")