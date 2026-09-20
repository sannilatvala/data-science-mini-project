import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = PROJECT_ROOT / "data" / "raw" / "helsinki"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = (
    PROCESSED_DATA
    / "helsinki_activities_candidate.csv"
)

HELSINKI_CITY = "helsinki"


CATEGORY_MAPPING = {
    "museums": "Museum",
    "theatres": "Theatre",
    "cinemas": "Cinema",
    "bowling alleys": "Bowling",
    "indoor climbing walls": "Climbing",
    "tennis court areas": "Tennis",
    "public indoor swimming pools": "Swimming",
    "indoor fitness centres": "Fitness",
    "martial arts halls": "Martial Arts",
    "ice skating fields": "Ice Skating",
    "ice skating routes": "Ice Skating",
    "golf courses": "Golf",
    "minigolf course": "Mini Golf",
    "disc golf courses": "Disc Golf",
    "galleries": "Art Gallery",
    "zoos": "Zoo",
    "dance facilities (sports recreation)": "Dance",
}


def load_json(filename):
    """Load a JSON file."""
    with open(
        RAW_DATA / filename,
        encoding="utf-8"
    ) as file:
        return json.load(file)


def load_data():
    """Load the Helsinki Service Map datasets."""

    units = pd.json_normalize(
        load_json("unit.json")
    )

    ontology_words = pd.DataFrame(
        load_json("ontologyword.json")
    )

    return units, ontology_words


def create_category_lookup(ontology_words):
    """Map ontology IDs to English category names."""

    return dict(
        zip(
            ontology_words["id"].astype(str),
            ontology_words["ontologyword_en"]
        )
    )


def get_activity_categories(
    ontology_ids,
    category_lookup
):
    """Convert ontology IDs into category names."""

    if ontology_ids is None:
        return []

    if isinstance(ontology_ids, str):
        ontology_ids = ontology_ids.split(",")

    if not isinstance(
        ontology_ids,
        (list, tuple)
    ):
        ontology_ids = list(ontology_ids)

    return [
        category_lookup.get(
            str(category_id).strip()
        )
        for category_id in ontology_ids
        if category_lookup.get(
            str(category_id).strip()
        )
    ]


def select_activity_categories(
    units,
    category_lookup
):
    """Select units belonging to our activity categories."""

    selected_rows = []

    for _, unit in units.iterrows():

        categories = get_activity_categories(
            unit["ontologyword_ids"],
            category_lookup
        )

        for category in categories:

            if category in CATEGORY_MAPPING:

                selected_rows.append({
                    "id": unit["id"],
                    "name": unit["name_fi"],
                    "activity_category":
                        CATEGORY_MAPPING[category],
                    "latitude": unit["latitude"],
                    "longitude": unit["longitude"],
                    "address":
                        unit["street_address_fi"],
                    "website":
                        unit["www_fi"],
                    "description":
                        unit["desc_fi"],
                })

    return pd.DataFrame(selected_rows)


def remove_obvious_non_activities(
    activities
):
    """
    Remove clearly irrelevant records that were included
    because they share an ontology category with the
    intended leisure activity.
    """

    name = (
        activities["name"]
        .fillna("")
        .str.lower()
    )

    category = activities[
        "activity_category"
    ]

    remove = pd.Series(
        False,
        index=activities.index
    )

    remove |= (
        (category == "Zoo")
        & ~name.str.contains(
            "korkeasaaren eläintarha",
            regex=False
        )
    )

    climbing_non_public = (
        "päiväkoti",
        "koulu",
        "yhteiskoulu",
        "valteri",
        "kuntoutuskeskus",
        "nuorisotalo",
    )

    for keyword in climbing_non_public:
        remove |= (
            (category == "Climbing")
            & name.str.contains(
                keyword,
                regex=False
            )
        )

    dance_non_activities = (
        "joogastudio",
        "joogasali",
        "pilates",
        "koulu",
        "lukio",
        "nuorisotalo",
        "olympiastadion",
        "urheiluhallit",
        "urhea-halli",
        "business college",
        "metropolia",
    )

    for keyword in dance_non_activities:
        remove |= (
            (category == "Dance")
            & name.str.contains(
                keyword,
                regex=False
            )
        )

    museum_non_museums = (
        "home hotel",
        "vallilan siirtolapuutarha",
        "helsingin diakonissalaitos",
        "gallery lemmetti",
        "kallion toiminnallinen",
        "suomen kansalaismuseo",
        "tennispalatsi",
    )

    for keyword in museum_non_museums:
        remove |= (
            (category == "Museum")
            & name.str.contains(
                keyword,
                regex=False
            )
        )

    gallery_non_galleries = (
        "kirjasto",
        "alkovi",
        "bar om'pu",
        "kansalliskirjasto",
        "arbis,",
        "annantalo",
        "kanneltalo",
        "caisa",
        "stoa",
        "vuotalo",
        "malmitalo",
        "kaapelitehdas",
        "oodi",
        "kulttuurilabra",
        "maunula-talo",
        "kulttuurilehtigalleria",
        "veistoskauppa",
        "craftcorner",
        "ateljee / boutique",
        "kukkakauppa",
    )

    for keyword in gallery_non_galleries:
        remove |= (
            (category == "Art Gallery")
            & name.str.contains(
                keyword,
                regex=False
            )
        )

    cinema_non_cinemas = (
        "flying cinema tour",
        "redi",
        "tennispalatsi",
        "kalasataman vapaakaupungin",
        "train factory",
    )

    for keyword in cinema_non_cinemas:
        remove |= (
            (category == "Cinema")
            & name.str.contains(
                keyword,
                regex=False
            )
        )

    swimming_non_public = (
        "suomalaisen yhteiskoulun",
        "laut tasaaren",
    )

    for keyword in swimming_non_public:
        remove |= (
            (category == "Swimming")
            & name.str.contains(
                keyword,
                regex=False
            )
        )

    remove |= (
        (category == "Disc Golf")
        & name.str.contains(
            "helsingin kristillinen koulu",
            regex=False
        )
    )

    remove |= (
        (category == "Disc Golf")
        & name.str.contains(
            "väliaikainen",
            regex=False
        )
    )

    return activities.loc[
        ~remove
    ].copy()


def remove_duplicates(
    activities
):
    """Remove duplicate records for the same activity."""

    activities = activities.drop_duplicates(
        subset=[
            "id",
            "activity_category"
        ]
    )

    activities = activities.drop_duplicates(
        subset=[
            "name",
            "address",
            "activity_category"
        ]
    )

    return activities

def clean_activities(activities):
    """Cleans activity descriptions by removing field numbers."""

    activities["name"] = (activities["name"].str.split("/", n=1).str[0].str.strip())

    return activities

def main():
    """Create the cleaned candidate catalogue."""

    PROCESSED_DATA.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        "Loading Helsinki Service Map data..."
    )

    units, ontology_words = load_data()

    print(
        f"Loaded {len(units):,} units."
    )

    units = units[
        units["address_city_fi"]
        .fillna("")
        .str.lower()
        == HELSINKI_CITY
    ].copy()

    print(
        f"Helsinki units: {len(units):,}"
    )

    category_lookup = (
        create_category_lookup(
            ontology_words
        )
    )

    activities = (
        select_activity_categories(
            units,
            category_lookup
        )
    )

    print(
        f"\nBefore cleaning: "
        f"{len(activities):,}"
    )

    activities = (
        remove_obvious_non_activities(
            activities
        )
    )

    activities = (
        clean_activities(activities)
    )

    activities = remove_duplicates(
        activities
    )

    print(
        f"After Stage 1 cleaning: "
        f"{len(activities):,}"
    )

    print(
        "\nActivities by category:"
    )

    print(
        activities[
            "activity_category"
        ]
        .value_counts()
        .sort_index()
        .to_string()
    )

    activities.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"\nSaved to:\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
