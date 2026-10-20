

import pandas as pd

# Load the traffic dataset
df = pd.read_csv(
    "data/traffic_ml_dataset.csv.gz",
    compression="gzip",
    parse_dates=["timestamp"]
)

# Define the spike threshold
spike_threshold = df["request_count"].quantile(0.95)

# Create the target: was the NEXT minute a spike?
df["next_minute_requests"] = df["request_count"].shift(-1)

df["next_minute_spike"] = (
    df["next_minute_requests"] > spike_threshold
).astype(int)

# Use information available before the next minute
df["requests_1_min_ago"] = df["request_count"]
df["requests_5_min_ago"] = df["request_count"].shift(4)
df["requests_15_min_ago"] = df["request_count"].shift(14)

df["rolling_avg_15_min"] = (
    df["request_count"].rolling(15).mean()
)

# Remove rows without enough historical information
df = df.dropna().reset_index(drop=True)

# Save the prepared dataset
df.to_csv(
    "data/spike_ml_dataset.csv",
    index=False
)

print("SCALESENSE AI - SPIKE MODEL DATA")
print("--------------------------------")
print("Total prepared rows:", len(df))
print("Spike cases:", int(df["next_minute_spike"].sum()))
print(
    "Normal cases:",
    int((df["next_minute_spike"] == 0).sum())
)
print("Saved to: data/spike_ml_dataset.csv")
