# Helsinki Leisure Activity Recommender

## 1. Introduction

Helsinki offers a wide range of leisure activities, but visitors may not know which options are available or which ones match their interests. This project develops a recommendation system for leisure activities in Helsinki, primarily targeting tourists and other visitors.

The project combines external user-rating data with Helsinki open data. Yelp data is used to learn general relationships between user preferences and activity categories, while Helsinki open data provides the actual local activities that can be recommended.

## 2. Background and Motivation

Visitors to a new city may have limited knowledge of available activities and may find it difficult to identify options matching their interests. A recommendation system can reduce this search effort by using information about user preferences to rank relevant activities.

The project investigates whether user-rating data from an external source can be used to learn general preference patterns and apply them to leisure activities available in Helsinki.

## 3. Research Question

> How can user preference information from external rating data be used to recommend leisure activities to visitors in Helsinki?

## 4. Data

### 4.1 Yelp Open Dataset

The [Yelp Open Dataset](https://business.yelp.com/data/resources/open-dataset/) provides businesses, categories, and user reviews and ratings. This project uses:

- Business data: `business_id`, `categories`
- Review data: `user_id`, `business_id`, `stars`

The `business_id` connects businesses with their ratings. Yelp is used to learn general relationships between user preferences and activity categories. Yelp users are not assumed to be the same users as those of the Helsinki application.

### 4.2 Helsinki Activity Data

The Helsinki data comes from the [Helsinki Region Infoshare Service Map REST API dataset](https://hri.fi/data/en/dataset/paakaupunkiseudun-palvelukartan-rest-rajapinta) and is downloaded through the [Helsinki Service Map REST API](https://www.hel.fi/palvelukarttaws/rest/v4/).

Four resources were downloaded:

- `unit` – service locations and their information
- `ontologyword` – individual service and activity categories
- `ontologytree` – category hierarchy
- `arealcity` – municipality information

The raw data contains 21,435 units, 1,113 ontology words, 1,593 ontology trees, and 14 area entries. Helsinki was identified as municipality ID 91. Restricting the unit data to Helsinki resulted in 12,252 units.

The `unit` data contains 60 fields, including names, categories, coordinates, addresses, descriptions, and contact information. All unit IDs are unique. The category fields contain no missing values, while some optional fields such as English names and descriptions have substantial missingness.

### 4.3 Combining the Data

The two datasets serve different purposes and cannot be directly joined through user or business IDs. Yelp provides historical rating information, while the Helsinki dataset provides the local recommendation catalogue.

Instead, the datasets are connected through comparable activity concepts. Yelp can therefore be used to learn general preference patterns, which can later be applied to representations of Helsinki activities.

## 5. Data Preprocessing

### 5.1 Yelp

The Yelp business data was reduced to `business_id` and `categories`, and businesses without category information were removed. This left **150,243 businesses**.

The review data was reduced to `user_id`, `business_id`, and `stars`. Reviews associated with removed businesses were excluded, leaving **6,989,591 reviews**. A total of **689 reviews** were removed.

Validation confirmed that the required fields contained no missing or empty values and that all **150,243 business IDs** in the review data existed in the processed business data. The data contains **1,987,685 unique users**, of whom **851,854 have multiple reviews**.

The Yelp data was processed in Python, with reviews read in chunks to reduce memory usage.

The business categories were also inspected to identify potentially relevant leisure categories. The dataset contains **1,311 unique categories** and **668,592 category assignments**. Relevant examples included Bowling, Cinema, Climbing, Fitness, Museums, Swimming Pools, Tennis, and other recreational categories. This inspection was exploratory; not all identified categories will necessarily be used in the final model.

### 5.2 Helsinki

The Helsinki preprocessing first restricted the Service Map units to Helsinki, leaving **12,252 units**. The ontology data was then explored to identify categories relevant to leisure activities.

Potential categories were initially identified using keyword-based searches of category names. The corresponding Service Map records were then inspected to determine whether they actually represented suitable leisure activities. Relevant categories were selected, while unsuitable or overly broad categories were excluded. These decisions were implemented in the preprocessing script so that the process is reproducible.

The selected categories were mapped to broader project activity categories, such as:

| Service Map category         | Project category |
| ---------------------------- | ---------------- |
| Museums                      | Museum           |
| Cinemas                      | Cinema           |
| Bowling alleys               | Bowling          |
| Indoor climbing walls        | Climbing         |
| Tennis court areas           | Tennis           |
| Public indoor swimming pools | Swimming         |
| Indoor fitness centres       | Fitness          |
| Golf courses                 | Golf             |
| Minigolf course              | Mini Golf        |
| Galleries                    | Art Gallery      |
| Zoos                         | Zoo              |
| Theatres                     | Theatre          |

The initial category selection produced **791 records**. After removing clearly irrelevant records and exact duplicates, **700 candidate activity records** remained across 16 categories.

| Activity category | Records |
| ----------------- | ------: |
| Art Gallery       |     101 |
| Bowling           |       8 |
| Cinema            |      20 |
| Climbing          |      11 |
| Dance             |      35 |
| Disc Golf         |      17 |
| Fitness           |      54 |
| Golf              |       6 |
| Ice Skating       |     126 |
| Martial Arts      |      49 |
| Mini Golf         |       7 |
| Museum            |      56 |
| Swimming          |      16 |
| Tennis            |     129 |
| Theatre           |      64 |
| Zoo               |       1 |
| **Total**         | **700** |

The cleaning was necessary because category information alone does not always identify suitable recommendation items. For example, the climbing category contained schools and other facilities, while the gallery category also contained libraries and cultural centres. Some categories were excluded entirely when they were too broad; for example, the gymnastics category contained 301 records but many represented ordinary school or community sports halls.

The exploration also showed that one physical venue can have multiple Service Map records. For example, individual tennis courts may appear as separate records even though they belong to the same venue. Therefore, the current 700-record dataset is considered a **candidate catalogue**, not the final set of recommendation items.

### 5.3 Activity Representation

The Yelp and Helsinki datasets use different category systems. For example, Helsinki uses categories such as _indoor fitness centres_ and _indoor climbing walls_, while Yelp contains categories such as _Gyms_, _Fitness & Instruction_, _Climbing_, and _Rock Climbing_.

Therefore, exact category-name matching is not sufficient. Instead, broader activity concepts such as **Fitness, Climbing, Tennis, Swimming, Museum, Cinema, Golf, and Mini Golf** can provide a common representation between the datasets.

The goal is not to force every category into an exact one-to-one match, but to create comparable activity representations that can be used when transferring preference information from Yelp to Helsinki activities.

## 6. Exploratory Data Analysis

The exploratory analysis focused on understanding the structure and suitability of both datasets before selecting the recommendation method.

For Yelp, the analysis examined business categories and the relationship between users, businesses, and reviews. The large number of users with multiple reviews makes it possible to investigate user-level rating patterns. At the same time, the large number of unrelated business categories means that using all Yelp categories would introduce substantial irrelevant information.

For Helsinki, the analysis focused on the Service Map ontology and the actual records belonging to potential leisure categories. The results showed substantial differences between categories. Some, such as bowling and golf, contained relatively small and clear sets of records, while categories such as tennis and ice skating contained many records because individual facilities or courts may be represented separately. Other categories required additional inspection because they contained a mixture of relevant and irrelevant locations.

These findings show that preprocessing and activity representation are important parts of the recommendation system. The number of raw Service Map records should not be interpreted as the number of unique leisure venues.

## 7. Recommendation System

### 7.1 Overall Approach

### 7.2 User Preference Representation

### 7.3 Activity Representation

### 7.4 Learning User Preferences

### 7.5 Generating Recommendations

## 8. Model Evaluation

### 8.1 Evaluation Strategy

### 8.2 Evaluation Metrics

### 8.3 Baseline

### 8.4 Results

## 9. Example Recommendations

## 10. Discussion

### 10.1 Main Findings

### 10.2 Strengths

### 10.3 Challenges

## 11. Limitations

### 11.1 Yelp and Helsinki User Differences

### 11.2 Category Mapping

### 11.3 Cold-Start Problem

### 11.4 Data Limitations

### 11.5 Evaluation Limitations

## 12. Ethical and Data Considerations

## 13. Future Work

## 14. Conclusion

## 15. References

## Appendix A: Project Structure

## Appendix B: Reproducibility
