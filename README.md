# Helsinki Leisure Activity Recommender

A recommendation system for leisure activities in Helsinki, primarily aimed at tourists and visitors.

## Project

The project uses:

- **Yelp Open Dataset** to learn user preferences and relationships between activity categories.
- **Helsinki Service Map open data** to provide local activities and venues.

Yelp users and Helsinki users are not directly matched. Instead, preferences are transferred through activity categories.

## Project Structure

```text
data-science-mini-project/

├── data/
│   ├── raw/
│   │   └── helsinki/
│   └── processed/
├── src/
│   ├── preprocess_yelp.py
│   ├── validate_yelp.py
│   ├── check_yelp_relationships.py
│   ├── download_helsinki_data.py
│   └── preprocess_helsinki.py
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

## Download and preprocess Yelp data

Download the [Yelp Open Dataset](https://business.yelp.com/data/resources/open-dataset/), extract the `.tar` file, and place it at:

```text
data/raw/yelp_dataset.tar
```

Then run:

```bash
python src/preprocess_yelp.py
```

The processed data will be saved in `data/processed/`.

## Download and preprocess Helsinki data

Helsinki data is obtained from the **Helsinki Service Map REST API**.

Download the required data:

```bash
python src/download_helsinki_data.py
```

This saves the raw data to:

```text
data/raw/helsinki/
```

Then preprocess it:

```bash
python src/preprocess_helsinki.py
```

The processed activity catalogue is saved as:

```text
data/processed/helsinki_activities_candidate.csv
```

## Data

The Yelp and Helsinki datasets are **not included in this repository**. Raw and processed data are excluded from Git.

Both datasets can be recreated using the download and preprocessing scripts above.

## Report

The project report is located in:

```text
report/report.md
```
