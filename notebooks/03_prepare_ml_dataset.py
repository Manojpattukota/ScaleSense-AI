

import pandas as pd
from pathlib import Path

# Locate project folders
project_folder = Path(__file__).resolve().parent.parent
input_file = project_folder / "data" / "nasa_traffic_cleaned.csv.gz"

# Load cleaned historical requests
df = pd.read_csv(
    input_file,
    compression="gzip",
    parse_dates=["timestamp"]
)

# Count requests per minute
traffic = (
    df.set_index("timestamp")
      .resample("1min")
      .size()
      .rename("request_count")
      .reset_index()
)

# Create time-based features
traffic["hour"] = traffic["timestamp"].dt.hour
traffic["day_of_month"] = traffic["timestamp"].dt.day
traffic["day_of_week"] = traffic["timestamp"].dt.dayofweek

# Save the prepared dataset
output_file = project_folder / "data" / "traffic_ml_dataset.csv.gz"

traffic.to_csv(
    output_file,
    index=False,
    compression="gzip"
)

print("SCALESENSE AI - ML DATASET")
print("-------------------------")
print("Total rows:", len(traffic))
print("Missing values:")
print(traffic.isna().sum())
print("\nFirst 5 rows:")
print(traffic.head().to_string(index=False))
print("\nSaved to:", output_file)
