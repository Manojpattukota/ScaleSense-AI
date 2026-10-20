

import pandas as pd

# Load the existing traffic dataset
df = pd.read_csv("data/traffic_ml_dataset.csv.gz")

# Keep only the columns needed for SQL analysis
sql_df = df[[
    "timestamp",
    "request_count",
    "hour",
    "day_of_month",
    "day_of_week"
]].copy()

# Save as a regular CSV file
sql_df.to_csv(
    "data/scalesense_traffic_sql.csv",
    index=False
)

print("SQL dataset created successfully!")
print("Total rows:", len(sql_df))
print("Columns:", list(sql_df.columns))
print(sql_df.head())
