

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    average_precision_score
)

# Load the prepared dataset
df = pd.read_csv("data/spike_ml_dataset.csv")

# Select the information the model can use
features = [
    "hour",
    "day_of_month",
    "day_of_week",
    "requests_1_min_ago",
    "requests_5_min_ago",
    "requests_15_min_ago",
    "rolling_avg_15_min"
]

X = df[features]
y = df["next_minute_spike"]

# Split chronologically: first 80% for training,
# final 20% for testing
split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

# Give greater weight to the rare spike cases
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

# Train the model
model.fit(X_train, y_train)

# Predict spikes on unseen, later data
y_prob = model.predict_proba(X_test)[:, 1]

# Compare two prediction thresholds
print("\nTHRESHOLD COMPARISON")
print("---------------------")

for test_threshold in [0.20, 0.50]:
    test_predictions = (
        y_prob >= test_threshold
    ).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_test,
        test_predictions,
        labels=[0, 1]
    ).ravel()

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0

    print(f"\nThreshold: {test_threshold:.2f}")
    print("Detected spikes:", tp)
    print("Missed spikes:", fn)
    print("False alarms:", fp)
    print("Precision:", round(precision * 100, 2), "%")
    print("Recall:", round(recall * 100, 2), "%")


# Flag a spike when predicted probability is at least 20%
threshold = 0.20
y_pred = (y_prob >= threshold).astype(int)

print("Decision threshold:", threshold)
# Evaluate the results
print("\nSCALESENSE AI - SPIKE MODEL RESULTS")
print("-----------------------------------")
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

print("\nCONFUSION MATRIX")
print("[[True normal, False alarm],")
print(" [Missed spike, Detected spike]]")
print(confusion_matrix(y_test, y_pred, labels=[0, 1]))

print("\nCLASSIFICATION REPORT")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Normal", "Spike"],
    zero_division=0
))

print(
    "Average precision:",
    round(average_precision_score(y_test, y_prob), 4)
)
# Save spike predictions for the dashboard
results = X_test.copy()

results["actual_spike"] = y_test.values
results["spike_probability"] = y_prob
results["predicted_spike"] = (y_prob >= 0.20).astype(int)

results.to_csv(
    "data/spike_predictions.csv",
    index=False
)

print("\nSpike predictions saved to data/spike_predictions.csv")