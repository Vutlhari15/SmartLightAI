
import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="SmartLight AI | Monitoring Centre",
    page_icon="💡",
    layout="wide"
)

# ---------------- PROFESSIONAL DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background-color: #F3F6FB;
}
[data-testid="stSidebar"] {
    background-color: #10243A;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #10243A;
}
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #DCE5F0;
    padding: 18px;
    border-radius: 12px;
}
div.stButton > button {
    background-color: #167D9A;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: 600;
}
div.stButton > button:hover {
    background-color: #105F76;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA AND MODEL ----------------
@st.cache_data
def load_dataset():
    return pd.read_csv("street_light_fault_prediction_dataset.csv")

@st.cache_resource
def load_model():
    with open("smartlight_model.pkl", "rb") as file:
        return pickle.load(file)

data = load_dataset()
saved_data = load_model()

model = saved_data["model"]
features = saved_data["features"]

environment_values = sorted(
    data["environmental_conditions"].astype(str).unique()
)
environment_codes = {
    value: index for index, value in enumerate(environment_values)
}

fault_names = {
    0: "No Fault",
    1: "Short Circuit",
    2: "Voltage Surge",
    3: "Bulb Failure",
    4: "Light Flickering"
}

# ---------------- SIDEBAR ----------------
st.sidebar.title("💡 SmartLight AI")
st.sidebar.caption("STREETLIGHT MONITORING CENTRE")
st.sidebar.divider()

st.sidebar.subheader("Monitoring Settings")
sample_size = st.sidebar.slider(
    "Records to analyse",
    min_value=10,
    max_value=100,
    value=20,
    step=10
)

faults_only = st.sidebar.checkbox(
    "Show only predicted faults",
    value=False
)

st.sidebar.divider()
st.sidebar.caption("Academic prototype • Synthetic dataset")
st.sidebar.caption("Not connected to live streetlights")

# ---------------- HEADER ----------------
st.title("💡 SmartLight AI")
st.subheader("AI-Powered Streetlight Fault Detection")

st.markdown(
    "An intelligent monitoring dashboard that classifies streetlight "
    "readings and helps identify records that may require maintenance."
)

st.info(
    f"Demonstration mode: the dataset is synthetic and contains "
    f"{len(data):,} records. Predictions use stored sample readings, "
    "not live municipal infrastructure."
)

col_a, col_b, col_c = st.columns(3)
col_a.metric("Dataset Records", f"{len(data):,}")
col_b.metric("Fault Categories", "5")
col_c.metric("Model Test Accuracy", "74.69%")

st.divider()

# ---------------- RUN MONITORING ----------------
if st.button("▶ Run AI Monitoring", use_container_width=True):

    sample = data.sample(n=sample_size).copy()

    original_environment = sample["environmental_conditions"].copy()

    sample["environmental_conditions"] = (
        sample["environmental_conditions"]
        .astype(str)
        .map(environment_codes)
    )

    predictions = model.predict(sample[features])

    results = pd.DataFrame({
        "Streetlight ID": [
            f"SL-{int(number):03d}"
            for number in sample["bulb_number"]
        ],
        "Timestamp": sample["timestamp"].values,
        "Power (W)": sample["power_consumption (Watts)"].values,
        "Voltage (V)": sample["voltage_levels (Volts)"].values,
        "Current (A)": sample["current_fluctuations (Amperes)"].values,
        "Temperature (°C)": sample["temperature (Celsius)"].values,
        "Weather": original_environment.values,
        "Dataset Label": [
            fault_names[int(label)] for label in sample["fault_type"]
        ],
        "AI Prediction": [
            fault_names[int(label)] for label in predictions
        ]
    })

    results["Prediction Match"] = (
        results["Dataset Label"] == results["AI Prediction"]
    ).map({True: "Match", False: "Different"})

    results["Maintenance Status"] = results["AI Prediction"].apply(
        lambda label: (
            "No action indicated"
            if label == "No Fault"
            else "Inspection recommended"
        )
    )

    st.success(
        f"Analysis complete. {sample_size} dataset records were analysed."
    )

    # ---------------- SUMMARY METRICS ----------------
    st.header("Monitoring Overview")

    fault_count = int((results["AI Prediction"] != "No Fault").sum())
    match_count = int((results["Prediction Match"] == "Match").sum())

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Records Analysed", len(results))
    m2.metric("Predicted Faults", fault_count)
    m3.metric("Predicted No Fault", len(results) - fault_count)
    m4.metric("Matches With Dataset Labels", f"{match_count}/{len(results)}")

    st.caption(
        "Matches compare predictions with the dataset's assigned labels. "
        "They are not a substitute for independent real-world testing."
    )

    # ---------------- FAULT DISTRIBUTION ----------------
    st.header("Fault Category Analysis")

    counts = (
        results["AI Prediction"]
        .value_counts()
        .reindex(list(fault_names.values()), fill_value=0)
    )

    chart_col, detail_col = st.columns([3, 2])

    with chart_col:
        st.subheader("Predicted Fault Distribution")
        st.bar_chart(counts)

    with detail_col:
        st.subheader("Category Counts")
        fault_summary = counts.rename_axis("Fault Category").reset_index(
            name="Records"
        )
        st.dataframe(
            fault_summary,
            hide_index=True,
            use_container_width=True
        )

    # ---------------- RECORDS AND ALERTS ----------------
    st.header("Streetlight Records")

    displayed_results = results.copy()

    if faults_only:
        displayed_results = displayed_results[
            displayed_results["AI Prediction"] != "No Fault"
        ]

    st.dataframe(
        displayed_results,
        hide_index=True,
        use_container_width=True
    )

    st.header("⚠️ Maintenance Alerts")

    alerts = results[results["AI Prediction"] != "No Fault"]

    if alerts.empty:
        st.success("No faults were predicted in this sample.")
    else:
        st.warning(
            f"{len(alerts)} record(s) have predicted faults. "
            "Inspection is recommended; predictions are not confirmed "
            "physical faults."
        )
        st.dataframe(
            alerts[[
                "Streetlight ID",
                "Timestamp",
                "AI Prediction",
                "Voltage (V)",
                "Current (A)",
                "Temperature (°C)",
                "Maintenance Status"
            ]],
            hide_index=True,
            use_container_width=True
        )

    # ---------------- DOWNLOAD REPORT ----------------
    st.header("Maintenance Report")

    report = results.copy()
    report.insert(
        0,
        "Report Generated",
        datetime.now().isoformat(timespec="seconds")
    )

    csv_data = report.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Full Monitoring Report (CSV)",
        data=csv_data,
        file_name="smartlight_maintenance_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.caption(
        "The report contains the sampled readings, dataset labels, "
        "AI predictions and recommended inspection status."
    )

else:
    st.subheader("Ready to Monitor")
    st.write(
        "Choose the number of records in the sidebar, then select "
        "**Run AI Monitoring** to analyse a sample from the dataset."
    )

# ---------------- MODEL PERFORMANCE ----------------
st.divider()
st.header("Model Performance")

st.write(
    "The Random Forest model was evaluated on a held-out test set "
    "of 6,862 records. Overall test accuracy was 74.69%."
)

performance = pd.DataFrame({
    "Fault Category": [
        "No Fault",
        "Short Circuit",
        "Voltage Surge",
        "Bulb Failure",
        "Light Flickering"
    ],
    "Precision": [0.85, 0.87, 0.67, 0.30, 0.76],
    "Recall": [0.80, 0.73, 0.55, 0.47, 0.77],
    "F1-Score": [0.82, 0.80, 0.60, 0.36, 0.76]
})

st.dataframe(
    performance.style.format({
        "Precision": "{:.2f}",
        "Recall": "{:.2f}",
        "F1-Score": "{:.2f}"
    }),
    hide_index=True,
    use_container_width=True
)

st.warning(
    "Bulb Failure is a weaker category for this model (F1-score 0.36). "
    "The model requires further improvement and real-world validation "
    "before it could support operational maintenance decisions."
)

st.caption(
    "SmartLight AI | Academic Capstone Prototype | "
    "Synthetic dataset | Not connected to live municipal infrastructure"
)
