
import gzip
import re
import pandas as pd
from pathlib import Path

# Locate our project and dataset
project_folder = Path(__file__).resolve().parent.parent
data_file = project_folder / "data" / "NASA_access_log_Aug95.gz"

# Pattern for extracting fields from NASA log records
pattern = re.compile(
    r'(\S+) \S+ \S+ '
    r'\[([^\]]+)\] '
    r'"(\S+) (\S+) ([^"]+)" '
    r'(\d{3}) (\S+)'
)

records = []

# Read the compressed file one line at a time
with gzip.open(data_file, "rt", encoding="latin-1") as file:
    for line in file:
        match = pattern.match(line)

        if match:
            host, timestamp, method, resource, protocol, status, size = (
                match.groups()
            )

            records.append({
                "host": host,
                "timestamp": timestamp,
                "method": method,
                "requested_resource": resource,
                "status_code": int(status),
                "response_bytes": (
                    int(size) if size.isdigit() else None
                )
            })

# Convert records into a table
df = pd.DataFrame(records)

# Convert timestamps into a datetime format
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    format="%d/%b/%Y:%H:%M:%S %z",
    errors="coerce"
)

print("\nSCALESENSE AI - STRUCTURED DATA")
print("--------------------------------")

print("\nFirst 5 records:")
print(df.head())

print("\nDataset information:")
print("Total parsed records:", len(df))
print("Missing timestamps:", df["timestamp"].isna().sum())
print("Missing response sizes:", df["response_bytes"].isna().sum())
# Save the structured dataset
output_file = project_folder / "data" / "nasa_traffic_cleaned.csv.gz"

df.to_csv(output_file, index=False, compression="gzip")

print("\nCleaned dataset saved successfully!")
print("Saved to:", output_file)
# Load the saved dataset
df = pd.read_csv(
    project_folder / "data" / "nasa_traffic_cleaned.csv.gz",
    compression="gzip",
    parse_dates=["timestamp"]
)

# Count requests per minute
traffic_per_minute = (
    df.set_index("timestamp")
      .resample("1min")
      .size()
      .reset_index(name="request_count")
)

print("\nTraffic per minute:")
print(traffic_per_minute.head(10))

print("\nTotal minutes:", len(traffic_per_minute))
print("Peak requests in one minute:", traffic_per_minute["request_count"].max())
# Find the 10 busiest minutes
top_10_minutes = traffic_per_minute.sort_values(
    by="request_count",
    ascending=False
).head(10)

print("\nTOP 10 BUSIEST MINUTES")
print("----------------------")
print(top_10_minutes.to_string(index=False))

# Analyze traffic by hour
traffic_per_hour = (
    df.set_index("timestamp")
      .resample("1h")
      .size()
      .reset_index(name="request_count")
)

# Find the 10 busiest hours
top_10_hours = traffic_per_hour.sort_values(
    by="request_count",
    ascending=False
).head(10)

print("\nTOP 10 BUSIEST HOURS")
print("--------------------")
print(top_10_hours.to_string(index=False))

# Find average traffic for each hour of the day
df["hour_of_day"] = df["timestamp"].dt.hour

average_traffic_by_hour = (
    df.groupby("hour_of_day")
      .size()
      .div(31)
      .reset_index(name="average_requests_per_hour")
)

print("\nAVERAGE TRAFFIC BY HOUR OF DAY")
print("--------------------------------")
print(average_traffic_by_hour.round(2).to_string(index=False))

# Identify the busiest typical hour
busiest_typical_hour = average_traffic_by_hour.loc[
    average_traffic_by_hour["average_requests_per_hour"].idxmax()
]

print("\nBusiest typical hour:", int(busiest_typical_hour["hour_of_day"]))
print(
    "Average requests during that hour:",
    round(busiest_typical_hour["average_requests_per_hour"], 2)
)

