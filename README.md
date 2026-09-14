# Helsinki Leisure Activity Recommender

A recommendation system for leisure activities in Helsinki, primarily aimed at tourists and visitors.

## Project

The project uses:

- **Yelp Open Dataset** to learn user preferences and activity-category relationships.
- **Helsinki open data** to provide local activities and venues.

Yelp users and Helsinki users are not directly matched. Instead, preferences are transferred through activity categories.

## Project Structure

```text
data-science-mini-project/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── preprocess_yelp.py
│   ├── validate_yelp.py
│   └── check_yelp_relationships.py
├── report/
│   └── report.md
├── README.md
├── requirements.txt
└── .gitignore
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### Download the Yelp dataset

Download the [Yelp Open Dataset](https://business.yelp.com/data/resources/open-dataset/).

Extract the `.tar` file from the downloaded ZIP and place it in:

```text
data/raw/yelp_dataset.tar
```

Run the preprocessing:

```bash
python src/preprocess_yelp.py
```

The processed data will be saved in `data/processed/`.

## Data

The Yelp dataset is **not included in this repository**. Raw and processed Yelp data are excluded from Git.

Helsinki activity data will be added and processed later.

## Report

The project report is located in:

```text
report/report.md
```
