
import pickle
import pandas as pd

# Load the trained model and its feature names
with open("smartlight_model.pkl", "rb") as file:
    saved_data = pickle.load(file)

model = saved_data["model"]
features = saved_data["features"]

# Example streetlight readings
streetlight_id = "SL-002"

readings = {
    "power_consumption (Watts)": 195.49,
    "voltage_levels (Volts)": 234.97,
    "current_fluctuations (Amperes)": 1.06,
    "temperature (Celsius)": 35.0,
    "current_fluctuations_env (Amperes)": 0.92,
    "environmental_conditions": "Rainy"
}

# Convert the environmental condition using
# the same category mapping used during training
df = pd.read_csv("street_light_fault_prediction_dataset.csv")
categories = sorted(
    df["environmental_conditions"].astype(str).unique()
)
environment_codes = {
    category: index for index, category in enumerate(categories)
}

readings["environmental_conditions"] = environment_codes[
    readings["environmental_conditions"]
]

# Arrange inputs in the correct order
input_data = pd.DataFrame([readings])[features]

# Predict the fault class
prediction = model.predict(input_data)[0]

print("===== SMARTLIGHT AI PREDICTION =====")
print("Streetlight ID:", streetlight_id)
print("Predicted fault type:", prediction)
print("Model prediction completed.")
