# Helsinki Leisure Activity Recommender

## 1. Introduction

Helsinki offers a wide range of leisure activities, but visitors may not know which activities are available or which ones match their interests. This project develops a recommendation system for leisure activities in Helsinki.

The application is primarily targeted at tourists and other visitors. By using information about user preferences, the system aims to help visitors discover suitable activities beyond the most well-known attractions.

The project combines external user-rating data with Helsinki-specific open data. Yelp data is used to learn relationships between user preferences and activity categories, while Helsinki open data provides the actual local activities that can be recommended.

## 2. Background and Motivation

Visitors to a new city have limited knowledge about the available activities and may have difficulty finding options that match their personal interests. A recommendation system can reduce this search effort by ranking activities according to user preferences.

The motivation of this project is to investigate whether user-rating data from an external source can be used to learn general preference patterns and apply these patterns to leisure activities available in Helsinki.

## 3. Research Question

How can user preference information from external rating data be used to recommend leisure activities to visitors in Helsinki?

## 4. Data

### 4.1 Yelp Open Dataset

The Yelp Open Dataset is used as an external source of user-rating data. It contains businesses, business categories, and user reviews and ratings.

For this project, the business data provides the `business_id` and `categories` fields, while the review data provides the `user_id`, `business_id`, and `stars` fields. The `business_id` is used to connect businesses with their user ratings.

The Yelp data is used to learn general relationships between user preferences and activity categories. Yelp users are not assumed to be the same users as those of the Helsinki application.

### 4.2 Helsinki Activity Data

Helsinki open data is used to provide information about actual leisure activities and venues available in Helsinki. This dataset forms the local activity catalogue from which recommendations can be generated.

### 4.3 Data Sources and Data Usage

The two datasets serve different purposes. Yelp provides historical user-rating information, while the Helsinki dataset provides the activities that can be recommended.

The datasets are therefore not directly combined through user IDs or business IDs. Instead, they will be connected through activity categories and other common features.

## 5. Data Preprocessing

### 5.1 Yelp Data Preprocessing

The Yelp dataset was downloaded as a TAR archive containing several JSON files. Only the business and review data were required for the initial recommendation system.

The business data was reduced to `business_id` and `categories`. Businesses without category information were removed, leaving **150,243 businesses**. The review data was reduced to `user_id`, `business_id`, and `stars`. Reviews associated with businesses that were removed during business preprocessing were also excluded, resulting in **6,989,591 reviews**. In total, **689 reviews** were removed for this reason.

A validation check confirmed that the required fields contained no missing or empty values. A relationship check also confirmed that all **150,243 business IDs** in the review data exist in the processed business data. The review data contains **1,987,685 unique users**, of whom **851,854 have multiple reviews**, confirming that individual users can have multiple ratings.

The preprocessing was implemented in Python. The review data was processed in chunks to avoid excessive memory usage, while ensuring that all retained reviews are associated with businesses that have available category information.

### 5.2 Helsinki Data Preprocessing

### 5.3 Category Processing and Mapping

### 5.4 Combining the Data

## 6. Exploratory Data Analysis

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
