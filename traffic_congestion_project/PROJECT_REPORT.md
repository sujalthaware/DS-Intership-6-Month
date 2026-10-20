# Internship Project Report: Traffic Congestion Prediction

## Objective
Build an intermediate-level application that collects real-time traffic flow observations, stores historical measurements, visualizes traffic conditions, and evaluates a machine-learning model.

## Methodology
1. Request road-segment flow data from a traffic API.
2. Store timestamp, location, current speed, free-flow speed, travel times, confidence, closure status, and derived congestion indicators.
3. Persist each collection round in SQLite and export CSV.
4. Visualize current and historical conditions in Streamlit.
5. Create a next-observation target for each road location.
6. Train a Random Forest classifier on earlier observations and evaluate on later observations.

## Evaluation
Fill in after collecting sufficient data and running the training script:
- Number of raw observations: [fill in]
- Number of sequential transitions: [fill in]
- Training rows: [fill in]
- Testing rows: [fill in]
- Accuracy: [fill in]
- Balanced accuracy: [fill in]
- Weighted F1: [fill in]

## Observations
Describe whether congestion differs by location or time. Discuss class imbalance and which categories the confusion matrix shows are difficult to predict. Do not claim model quality from a tiny dataset.

## Limitations
Live traffic access requires an API key and is subject to provider quotas and terms. The default coordinate is only an example. The model predicts the class at the next collected observation rather than at a fixed future horizon.

## Conclusion
The project demonstrates an end-to-end data science workflow with live data ingestion, storage, feature engineering, machine-learning evaluation, and dashboard visualization.
