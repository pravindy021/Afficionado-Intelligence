# Model Documentation

## Segmentation
Median revenue and median units define the documented segment thresholds. Stars, Hidden Gems,
Premium Performers, Volume Drivers, and Underperformers include explainable reasons.

## Clustering
Features: revenue, quantity, average price. StandardScaler, K-Means, PCA 2D visualization,
elbow inertia, and silhouette score. Random state is 42.

## Anomaly detection
IQR, Z-score, and Isolation Forest are used only for statistical review. Anomalies are not
classified as fraud or operational failure.

## Forecasting
Forecasting is deliberately unsupported for the source dataset because it has no calendar date
or repeated-day history. The system does not invent dates or prediction accuracy.

## Scenario engine
Pricing changes are explicit arithmetic hypotheses. No elasticity or causal model is claimed.
