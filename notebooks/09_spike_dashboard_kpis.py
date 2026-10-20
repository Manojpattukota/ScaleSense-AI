

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/spike_predictions.csv")

actual = df["actual_spike"]
predicted = df["predicted_spike"]

detected = ((actual == 1) & (predicted == 1)).sum()
missed = ((actual == 1) & (predicted == 0)).sum()
false_alarms = ((actual == 0) & (predicted == 1)).sum()
correct_normal = ((actual == 0) & (predicted == 0)).sum()

total = len(df)

recall = detected / (detected + missed) * 100
precision = detected / (detected + false_alarms) * 100
accuracy = (detected + correct_normal) / total * 100

fig, ax = plt.subplots(figsize=(10, 5))
ax.axis("off")

ax.set_title(
    "ScaleSense AI | Traffic Spike Monitoring",
    fontsize=17,
    fontweight="bold",
    pad=25
)

kpis = [
    ("Spike Recall", f"{recall:.1f}%"),
    ("Spike Precision", f"{precision:.1f}%"),
    ("Accuracy", f"{accuracy:.1f}%"),
    ("Missed Spikes", f"{missed}")
]

positions = [
    (0.25, 0.65),
    (0.75, 0.65),
    (0.25, 0.30),
    (0.75, 0.30)
]

for (label, value), (x, y) in zip(kpis, positions):
    ax.text(
        x, y, value,
        ha="center", va="center",
        fontsize=23, fontweight="bold",
        transform=ax.transAxes
    )
    ax.text(
        x, y - 0.10, label,
        ha="center", va="center",
        fontsize=11,
        transform=ax.transAxes
    )

plt.tight_layout()
plt.savefig(
    "dashboards/spike_dashboard_kpis.png",
    dpi=150,
    bbox_inches="tight"
)
plt.show()

print("Dashboard saved to dashboards/spike_dashboard_kpis.png")
print(f"Spike recall: {recall:.2f}%")
print(f"Spike precision: {precision:.2f}%")
print(f"Accuracy: {accuracy:.2f}%")
