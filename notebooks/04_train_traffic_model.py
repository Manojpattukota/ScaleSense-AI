
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Locate and load the prepared dataset
project_folder = Path(__file__).resolve().parent.parent
data_file = project_folder / "data" / "traffic_ml_dataset.csv.gz"

df = pd.read_csv(
    data_file,
    compression="gzip",
    parse_dates=["timestamp"]
)


# Create features from previous traffic counts
df["requests_1_min_ago"] = df["request_count"].shift(1)
df["requests_5_min_ago"] = df["request_count"].shift(5)
df["requests_15_min_ago"] = df["request_count"].shift(15)

# Calculate recent traffic change
df["traffic_change_5_min"] = (
    df["request_count"].shift(1)
    - df["request_count"].shift(6)
)


# Average traffic during the previous 15 minutes.
# shift(1) prevents the current minute from leaking into this feature.
df["rolling_avg_15_min"] = (
    df["request_count"]
      .shift(1)
      .rolling(window=15)
      .mean()
)


features = [
    "hour",
    "day_of_month",
    "day_of_week",
    "requests_1_min_ago",
    "requests_5_min_ago",
    "requests_15_min_ago",
    "rolling_avg_15_min",
    "traffic_change_5_min"
]

target = "request_count"

# Remove rows without sufficient historical information
df = df.dropna().reset_index(drop=True)

X = df[features]
y = df[target]


X = df[features]
y = df[target]

# Keep time order: first 80% for training, last 20% for testing
split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]
y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

# Train the model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Predict traffic for the test period
predictions = model.predict(X_test)

# Evaluate prediction accuracy
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print("\nSCALESENSE AI - MODEL RESULTS")
print("-----------------------------")
print("Mean Absolute Error (MAE):", round(mae, 2))
print("Root Mean Squared Error (RMSE):", round(rmse, 2))

# Compare actual and predicted traffic
comparison = pd.DataFrame({
    "timestamp": df["timestamp"].iloc[split_index:].reset_index(drop=True),
    "actual_requests": y_test.values,
    "predicted_requests": predictions.round(2)
})

print("\nFirst 10 predictions vs actual:")
print(comparison.head(10).to_string(index=False))

# Save all test predictions
predictions_file = (
    project_folder / "data" / "traffic_predictions.csv"
)

comparison.to_csv(predictions_file, index=False)

# Plot the first 500 test minutes
plot_data = comparison.head(500)

plt.figure(figsize=(14, 6))

plt.plot(
    plot_data["timestamp"],
    plot_data["actual_requests"],
    label="Actual Traffic",
    linewidth=1
)

plt.plot(
    plot_data["timestamp"],
    plot_data["predicted_requests"],
    label="Predicted Traffic",
    linewidth=1
)

plt.title("ScaleSense AI - Actual vs Predicted Traffic")
plt.xlabel("Time")
plt.ylabel("Requests per Minute")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

chart_file = (
    project_folder / "dashboards" / "actual_vs_predicted.png"
)

plt.savefig(chart_file, dpi=150)
plt.show()

print("\nPredictions saved to:", predictions_file)
print("Comparison chart saved to:", chart_file)

# Find the 10 highest-traffic minutes in the test period
top_10_actual_peaks = comparison.sort_values(
    by="actual_requests",
    ascending=False
).head(10)

print("\nTOP 10 ACTUAL TRAFFIC PEAKS IN TEST DATA")
print("----------------------------------------")
print(
    top_10_actual_peaks[
        ["timestamp", "actual_requests", "predicted_requests"]
    ].to_string(index=False)
)

# Measure how much the model underestimates traffic
comparison["underestimation"] = (
    comparison["actual_requests"]
    - comparison["predicted_requests"]
)

# Keep only minutes where actual traffic exceeded the prediction
underestimated = comparison[
    comparison["underestimation"] > 0
]

print("\nPEAK UNDERSTIMATION ANALYSIS")
print("----------------------------")

print(
    "Minutes where traffic was underestimated:",
    len(underestimated)
)

print(
    "Percentage of test minutes underestimated:",
    round(len(underestimated) / len(comparison) * 100, 2),
    "%"
)

print(
    "Largest underestimation:",
    round(comparison["underestimation"].max(), 2),
    "requests per minute"
)
# Analyze traffic distribution
print("\nTRAFFIC DISTRIBUTION")
print("--------------------")

print("Average requests:", round(df["request_count"].mean(), 2))
print("Median requests:", round(df["request_count"].median(), 2))
print("95th percentile:", round(df["request_count"].quantile(0.95), 2))
print("99th percentile:", round(df["request_count"].quantile(0.99), 2))
print("Maximum requests:", df["request_count"].max())