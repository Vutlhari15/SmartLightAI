import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

st.set_page_config(
    page_title="SmartLight AI",
    page_icon="💡",
    layout="wide"
)

# Load the trained model
with open("smartlight_model.pkl", "rb") as file:
    saved_data = pickle.load(file)

model = saved_data["model"]
features = saved_data["features"]

# Load the dataset
data = pd.read_csv("street_light_fault_prediction_dataset.csv")

# Encode environmental conditions consistently
environment_values = sorted(
    data["environmental_conditions"].astype(str).unique()
)
environment_codes = {
    value: index for index, value in enumerate(environment_values)
}

# Fault names from the dataset description
fault_names = {
    0: "No Fault",
    1: "Short Circuit",
    2: "Voltage Surge",
    3: "Bulb Failure",
    4: "Light Flickering"
}

# Dashboard heading
st.title("💡 SmartLight AI")
st.subheader("AI-Powered Streetlight Fault Detection")

st.info(
    "Dataset demonstration: this dataset is synthetic. "
    "Predictions use recorded sample readings, not live municipal "
    "streetlights."
)

st.write(f"Dataset records available: **{len(data):,}**")

st.write(
    "Fault categories: 💡 No Fault | ⚡ Short Circuit | "
    "🔌 Voltage Surge | 💡 Bulb Failure | ✨ Light Flickering"
)

# Run monitoring only when the button is clicked
if st.button("Run Streetlight Monitoring"):

    # Select 10 sample records
    sample = data.sample(n=10).copy()

    # Keep original environmental values for display
    original_environment = sample["environmental_conditions"].copy()

    # Encode environmental conditions for the model
    sample["environmental_conditions"] = (
        sample["environmental_conditions"]
        .astype(str)
        .map(environment_codes)
    )

    # Predict fault labels
    X = sample[features]
    predictions = model.predict(X)

    # Build the results table
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
        "Environmental Conditions": original_environment.values,
        "Actual Fault Type": [
            fault_names[int(label)]
            for label in sample["fault_type"]
        ],
        "AI Predicted Fault Type": [
            fault_names[int(prediction)]
            for prediction in predictions
        ]
    })

    # Compare predictions with dataset labels
    results["Prediction Match"] = (
        results["Actual Fault Type"]
        == results["AI Predicted Fault Type"]
    ).map({
        True: "Match",
        False: "Different"
    })

    # Monitoring overview
    st.divider()
    st.header("📊 Monitoring Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Records Analysed", len(results))

    col2.metric(
        "Predictions Matching Labels",
        int((results["Prediction Match"] == "Match").sum())
    )

    col3.metric(
        "Predictions Differing From Labels",
        int((results["Prediction Match"] == "Different").sum())
    )

    # Results table
    st.subheader("Streetlight Readings and AI Predictions")
    st.dataframe(results, width="stretch")

    # Maintenance alerts
    st.subheader("⚠️ Maintenance Alerts")

    faults_detected = results[
        results["AI Predicted Fault Type"] != "No Fault"
    ]

    if not faults_detected.empty:
        st.warning(
            f"{len(faults_detected)} of the 10 records have "
            "a predicted fault and may need further inspection."
        )

        st.dataframe(
            faults_detected[
                [
                    "Streetlight ID",
                    "AI Predicted Fault Type",
                    "Prediction Match"
                ]
            ],
            width="stretch"
        )
    else:
        st.success(
            "No faults predicted in this monitoring run."
        )

    # Predicted fault distribution
    st.subheader("📈 Predicted Fault Distribution")

    chart_data = (
        results["AI Predicted Fault Type"]
        .value_counts()
        .rename_axis("Predicted Fault Type")
        .to_frame("Number of Records")
    )

    st.bar_chart(chart_data)

    # Download report
    report = results.copy()
    report.insert(
        0,
        "Report Generated",
        datetime.now().isoformat(timespec="seconds")
    )

    st.download_button(
        label="📥 Download Maintenance Report",
        data=report.to_csv(index=False).encode("utf-8"),
        file_name="smartlight_dashboard_report.csv",
        mime="text/csv"
    )

else:
    st.write(
        "Click **Run Streetlight Monitoring** to analyse "
        "10 records from the dataset."
    )

# Footer
st.caption(
    "SmartLight AI | Academic Capstone Prototype | "
    "Synthetic dataset demonstration; not connected to live streetlights."
)