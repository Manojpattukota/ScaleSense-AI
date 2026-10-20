

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Locate the project and load cleaned data
project_folder = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    project_folder / "data" / "nasa_traffic_cleaned.csv.gz",
    compression="gzip",
    parse_dates=["timestamp"]
)

# Calculate average requests per hour of day
df["hour_of_day"] = df["timestamp"].dt.hour

average_traffic = (
    df.groupby("hour_of_day")
      .size()
      .div(31)
)

# Create the chart
plt.figure(figsize=(12, 6))
plt.plot(
    average_traffic.index,
    average_traffic.values,
    marker="o"
)

plt.title("ScaleSense AI - Average Web Traffic by Hour")
plt.xlabel("Hour of Day (0-23)")
plt.ylabel("Average Requests per Hour")
plt.xticks(range(24))
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save chart in dashboards folder
chart_path = project_folder / "dashboards" / "average_traffic_by_hour.png"
plt.savefig(chart_path, dpi=150)
plt.show()

print("Chart saved to:", chart_path)
