import math
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ScaleSense AI",
    page_icon="📊",
    layout="wide"
)
# Sidebar
st.sidebar.title("⚙️ Dashboard Settings")

st.sidebar.write("Project: ScaleSense AI")

st.sidebar.info(
    "Model: Random Forest Classifier"
)
df = pd.read_csv("data/spike_predictions.csv")
# Interactive prediction threshold
threshold = st.sidebar.slider(
    "Prediction Threshold",
    min_value=0.05,
    max_value=0.95,
    value=0.20,
    step=0.05
)

st.sidebar.write(
    f"Selected threshold: {threshold:.0%}"
)

# Recalculate predictions at the selected threshold
adjusted_predictions = (
    df["spike_probability"] >= threshold
).astype(int)

st.sidebar.metric(
    "Predicted Spikes",
    int(adjusted_predictions.sum())
)

st.sidebar.write(
    "Goal: Catch as many traffic spikes as possible."
)
st.title("🚀 ScaleSense AI")
st.subheader(
    "AI-Powered Peak Traffic Prediction & Capacity Planning System"
)

st.write(
    "Monitor website traffic, detect traffic spikes, "
    "and evaluate our machine-learning model."
)

# Load the model predictions


st.success("Spike prediction data loaded successfully!")
# Update predictions using the selected threshold
df["predicted_spike"] = (
    df["spike_probability"] >= threshold
).astype(int)
# Traffic risk status
predicted_spike_count = int(df["predicted_spike"].sum())

if predicted_spike_count > 1000:
    st.warning("⚠️ High Traffic Risk: Many potential spikes detected.")
elif predicted_spike_count > 500:
    st.info("🔎 Moderate Traffic Risk: Several potential spikes detected.")
else:
    st.success("✅ Low Traffic Risk: Fewer potential spikes detected.")
st.caption(
    f"The model flagged {predicted_spike_count:,} possible spikes "
    f"at the selected threshold. These are predictions, not confirmed incidents."
)
# Calculate dashboard KPIs
detected = (
    (df["actual_spike"] == 1) &
    (df["predicted_spike"] == 1)
).sum()

missed = (
    (df["actual_spike"] == 1) &
    (df["predicted_spike"] == 0)
).sum()

false_alarms = (
    (df["actual_spike"] == 0) &
    (df["predicted_spike"] == 1)
).sum()

total_records = len(df)

# Compare model performance at two thresholds
st.subheader("⚖️ Threshold Comparison")

comparison_rows = []

for test_threshold in [0.20, 0.50]:
    test_predictions = (
        df["spike_probability"] >= test_threshold
    ).astype(int)

    actual = df["actual_spike"]

    tp = ((actual == 1) & (test_predictions == 1)).sum()
    fn = ((actual == 1) & (test_predictions == 0)).sum()
    fp = ((actual == 0) & (test_predictions == 1)).sum()

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0

    comparison_rows.append({
        "Threshold": f"{test_threshold:.2f}",
        "Detected Spikes": int(tp),
        "Missed Spikes": int(fn),
        "False Alarms": int(fp),
        "Precision (%)": round(precision * 100, 2),
        "Recall (%)": round(recall * 100, 2)
    })

comparison_df = pd.DataFrame(comparison_rows)

st.dataframe(
    comparison_df,
    hide_index=True,
    use_container_width=True
)


# Display KPI cards
st.subheader("📊 Model Performance Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Test Records", total_records)
col2.metric("Spikes Detected", int(detected))
col3.metric("Spikes Missed", int(missed))
col4.metric("False Alarms", int(false_alarms))
# Calculate performance percentages
recall = detected / (detected + missed) * 100
precision = detected / (detected + false_alarms) * 100

correct_normal = (
    (df["actual_spike"] == 0) &
    (df["predicted_spike"] == 0)
).sum()

accuracy = (
    (detected + correct_normal) / total_records
) * 100

# Display performance metrics
st.subheader("🎯 Model Performance Scores")

m1, m2, m3 = st.columns(3)

m1.metric("Spike Recall", f"{recall:.2f}%")
m2.metric("Spike Precision", f"{precision:.2f}%")
m3.metric("Overall Accuracy", f"{accuracy:.2f}%")

# Show the dataset
# Filter prediction results
st.subheader("📋 Spike Prediction Data")

prediction_filter = st.selectbox(
    "Choose prediction type",
    [
        "All Records",
        "Actual Spikes",
        "Predicted Spikes",
        "Missed Spikes",
        "False Alarms"
    ]
)

if prediction_filter == "All Records":
    filtered_df = df

elif prediction_filter == "Actual Spikes":
    filtered_df = df[df["actual_spike"] == 1]

elif prediction_filter == "Predicted Spikes":
    filtered_df = df[df["predicted_spike"] == 1]

elif prediction_filter == "Missed Spikes":
    filtered_df = df[
        (df["actual_spike"] == 1) &
        (df["predicted_spike"] == 0)
    ]

else:
    filtered_df = df[
        (df["actual_spike"] == 0) &
        (df["predicted_spike"] == 1)
    ]

st.write(f"Showing {len(filtered_df)} records")

st.dataframe(
    filtered_df.head(20),
    use_container_width=True
)
# Download filtered prediction records
csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv_data,
    file_name="scalesense_predictions.csv",
    mime="text/csv"
)
# Traffic spike detection chart
st.subheader("📉 Traffic Spike Detection Analysis")

chart_data = pd.DataFrame({
    "Category": [
        "Spikes Detected",
        "Spikes Missed",
        "False Alarms"
    ],
    "Count": [
        int(detected),
        int(missed),
        int(false_alarms)
    ]
})

st.bar_chart(
    chart_data,
    x="Count",
    y="Category",
    horizontal=True,
    x_label="Number of Records",
    y_label="Detection Category"
)

# Spike prediction probability distribution
st.subheader("🔍 Spike Prediction Probabilities")
st.write("Explore how the model assigns spike probabilities.")

probability_bins = pd.cut(
    df["spike_probability"],
    bins=[
        0, 0.1, 0.2, 0.3, 0.4, 0.5,
        0.6, 0.7, 0.8, 0.9, 1.0
    ],
    include_lowest=True
)

probability_counts = (
    probability_bins.value_counts().sort_index()
)

chart_data = pd.DataFrame({
    "Probability Range": probability_counts.index.astype(str),
    "Number of Records": probability_counts.values
})

st.bar_chart(
    chart_data,
    x="Probability Range",
    y="Number of Records",
    x_label="Spike Probability Range",
    y_label="Number of Records"
)

# Capacity Planning Estimate
st.subheader("🏗️ Traffic Capacity Planning")

st.write(
    "Estimate a planning target based on historical traffic. "
    "This is an estimate, not measured server capacity."
)

# Load historical traffic data
traffic_df = pd.read_csv("data/traffic_ml_dataset.csv.gz")

peak_traffic = int(traffic_df["request_count"].max())
p95_traffic = float(traffic_df["request_count"].quantile(0.95))


safety_factor = st.slider(
    "Capacity Safety Buffer (%)",
    min_value=10,
    max_value=100,
    value=30,
    step=10
)

growth_rate = st.slider(
    "Expected Traffic Growth (%)",
    min_value=0,
    max_value=100,
    value=20,
    step=10
)

future_peak = peak_traffic * (1 + growth_rate / 100)
if growth_rate >= 60:
    st.warning(
        "⚠️ High Growth Scenario: "
        "Review capacity requirements and perform load testing."
    )
elif growth_rate >= 40:
    st.info(
        "📈 Elevated Growth Scenario: "
        "Review your capacity planning assumptions."
    )


recommended_capacity = math.ceil(
    future_peak * (1 + safety_factor / 100)
)


col1, col2, col3 = st.columns(3)

col1.metric(
    "Historical Peak",
    f"{peak_traffic:,} requests/min"
)

col2.metric(
    "Projected Peak",
    f"{math.ceil(future_peak):,} requests/min"
)

col3.metric(
    "Planning Target",
    f"{recommended_capacity:,} requests/min"
)

st.caption(
    f"Estimate based on {growth_rate}% expected traffic growth "
    f"and a {safety_factor}% safety buffer. "
    "This is a planning estimate, not measured server capacity. "
    "Validate with load testing before deployment."
)


st.caption(
    f"The planning target adds a {safety_factor}% buffer "
    "to the highest observed one-minute request count. "
    "Validate it with load testing before using it for deployment."
)

# Download capacity planning report
capacity_report = pd.DataFrame([{
    "Historical Peak (requests/min)": peak_traffic,
    "Expected Traffic Growth (%)": growth_rate,
    "Projected Peak (requests/min)": math.ceil(future_peak),
    "Safety Buffer (%)": safety_factor,
    "Recommended Capacity (requests/min)": recommended_capacity
}])

st.download_button(
    label="📥 Download Capacity Planning Report",
    data=capacity_report.to_csv(index=False),
    file_name="scalesense_capacity_report.csv",
    mime="text/csv"
)

# Visual capacity comparison
st.subheader("📊 Capacity Planning Comparison")

capacity_chart = pd.DataFrame({
    "Traffic Measure": [
        "Historical Peak",
        "Projected Peak",
        "Planning Target"
    ],
    "Requests per Minute": [
        peak_traffic,
        math.ceil(future_peak),
        recommended_capacity
    ]
})

st.bar_chart(
    capacity_chart,
    x="Traffic Measure",
    y="Requests per Minute",
    x_label="Traffic Measure",
    y_label="Requests per Minute"
)

# Traffic Growth Scenario Analysis
st.subheader("📈 Traffic Growth Scenarios")

growth_scenarios = [0, 20, 40, 60, 80, 100]

scenario_rows = []

for growth in growth_scenarios:
    projected = math.ceil(peak_traffic * (1 + growth / 100))
    capacity = math.ceil(projected * (1 + safety_factor / 100))

    scenario_rows.append({
        "Traffic Growth (%)": growth,
        "Projected Peak (requests/min)": projected,
        "Planning Target (requests/min)": capacity
    })

scenario_df = pd.DataFrame(scenario_rows)

st.dataframe(
    scenario_df,
    hide_index=True,
    use_container_width=True
)

# Historical Traffic Pattern
st.subheader("🕒 Historical Traffic Pattern")

traffic_df["timestamp"] = pd.to_datetime(
    traffic_df["timestamp"]
)

traffic_df["hour"] = traffic_df["timestamp"].dt.hour

hourly_traffic = (
    traffic_df.groupby("hour")["request_count"]
    .mean()
    .reset_index()
)

hourly_traffic.columns = [
    "Hour of Day",
    "Average Requests per Minute"
]

st.line_chart(
    hourly_traffic,
    x="Hour of Day",
    y="Average Requests per Minute",
    x_label="Hour of Day (0–23)",
    y_label="Average Requests per Minute"
)

# Peak Hour Summary
st.subheader("🚦 Peak Hour Analysis")

busiest_hour = hourly_traffic.loc[
    hourly_traffic["Average Requests per Minute"].idxmax()
]

quietest_hour = hourly_traffic.loc[
    hourly_traffic["Average Requests per Minute"].idxmin()
]

col1, col2 = st.columns(2)

col1.metric(
    "Busiest Hour",
    f"{int(busiest_hour['Hour of Day']):02d}:00",
    f"{busiest_hour['Average Requests per Minute']:.1f} requests/min"
)

col2.metric(
    "Quietest Hour",
    f"{int(quietest_hour['Hour of Day']):02d}:00",
    f"{quietest_hour['Average Requests per Minute']:.1f} requests/min"
)

# Explore Traffic by Hour
st.subheader("🔎 Explore Traffic by Hour")

selected_hour = st.selectbox(
    "Select an hour",
    list(range(24)),
    format_func=lambda hour: f"{hour:02d}:00"
)

hour_records = traffic_df[
    traffic_df["hour"] == selected_hour
]

st.metric(
    "Total Requests During Selected Hour",
    f"{hour_records['request_count'].sum():,}"
)

st.metric(
    "Average Requests per Minute",
    f"{hour_records['request_count'].mean():.2f}"
)

st.caption(
    "These results summarize historical observations "
    "for the selected hour across the dataset."
)

# Traffic Details for Selected Hour
st.subheader("📊 Traffic Details for Selected Hour")

if not hour_records.empty:
    busiest_minute = hour_records.loc[
        hour_records["request_count"].idxmax()
    ]

    quietest_minute = hour_records.loc[
        hour_records["request_count"].idxmin()
    ]

    col1, col2 = st.columns(2)

    col1.metric(
        "Highest Requests in One Minute",
        int(busiest_minute["request_count"])
    )

    col2.metric(
        "Lowest Requests in One Minute",
        int(quietest_minute["request_count"])
    )

# Traffic Intensity Classification
st.subheader("🚦 Traffic Intensity")

average_selected_traffic = hour_records["request_count"].mean()

if average_selected_traffic < 30:
    st.success("Low Traffic: Historical request levels are relatively low.")
elif average_selected_traffic < 60:
    st.info("Moderate Traffic: Monitor traffic trends.")
else:
    st.warning("High Traffic: Review capacity planning assumptions.")

st.caption(
    "These are illustrative project thresholds based on average "
    "requests per minute, not universal server-capacity limits."
)

# Traffic Intensity Distribution
st.subheader("📊 Traffic Intensity Distribution")

hourly_traffic["Traffic Intensity"] = hourly_traffic[
    "Average Requests per Minute"
].apply(
    lambda value: (
        "Low"
        if value < 30
        else "Moderate"
        if value < 60
        else "High"
    )
)

intensity_counts = (
    hourly_traffic["Traffic Intensity"]
    .value_counts()
    .reindex(["Low", "Moderate", "High"], fill_value=0)
)

intensity_chart = pd.DataFrame({
    "Traffic Intensity": intensity_counts.index,
    "Number of Hours": intensity_counts.values
})

st.bar_chart(
    intensity_chart,
    x="Traffic Intensity",
    y="Number of Hours"
)
