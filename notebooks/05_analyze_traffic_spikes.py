

import pandas as pd

# Load the existing traffic dataset
df = pd.read_csv(
    "data/traffic_ml_dataset.csv.gz",
    compression="gzip"
)

# Define our initial spike threshold
spike_threshold = df["request_count"].quantile(0.95)

# Mark minutes that exceed the threshold
df["is_spike"] = df["request_count"] > spike_threshold

# Count normal and spike minutes
spike_count = df["is_spike"].sum()
normal_count = len(df) - spike_count

print("\nSCALESENSE AI - TRAFFIC SPIKE ANALYSIS")
print("--------------------------------------")
print("Total minutes:", len(df))
print("Spike threshold:", spike_threshold)
print("Spike minutes:", spike_count)
print("Normal minutes:", normal_count)
print(
    "Spike percentage:",
    round(spike_count / len(df) * 100, 2),
    "%"
)

# Show the five busiest minutes
print("\nTOP 5 TRAFFIC SPIKES")
print(
    df.nlargest(5, "request_count")[
        ["timestamp", "request_count", "is_spike"]
    ].to_string(index=False)
)
