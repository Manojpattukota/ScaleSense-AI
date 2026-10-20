

import pandas as pd
import matplotlib.pyplot as plt

# Load saved predictions
df = pd.read_csv("data/spike_predictions.csv")

# Count prediction outcomes
actual = df["actual_spike"]
predicted = df["predicted_spike"]

detected = ((actual == 1) & (predicted == 1)).sum()
missed = ((actual == 1) & (predicted == 0)).sum()
false_alarms = ((actual == 0) & (predicted == 1)).sum()
correct_normal = ((actual == 0) & (predicted == 0)).sum()

# Display the numbers
print("SCALESENSE AI - DASHBOARD SUMMARY")
print("---------------------------------")
print("Detected spikes:", detected)
print("Missed spikes:", missed)
print("False alarms:", false_alarms)
print("Correct normal predictions:", correct_normal)

# Create a bar chart
labels = [
    "Detected spikes",
    "Missed spikes",
    "False alarms",
    "Correct normal"
]

values = [
    detected,
    missed,
    false_alarms,
    correct_normal
]

plt.figure(figsize=(10, 6))
plt.bar(labels, values)
plt.title("ScaleSense AI - Traffic Spike Detection")
plt.ylabel("Number of minutes")
plt.xticks(rotation=15)
plt.tight_layout()

plt.savefig("dashboards/spike_detection_summary.png")
plt.show()

print("\nChart saved to dashboards/spike_detection_summary.png")
