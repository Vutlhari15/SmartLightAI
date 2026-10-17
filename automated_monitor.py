
import csv
import pickle
import random
from datetime import datetime

# Load the trained machine-learning model
with open("smartlight_model.pkl", "rb") as file:
    model = pickle.load(file)

# Generate simulated sensor readings
def generate_sensor_readings():
    fault_type = random.choice([
        "normal",
        "normal",
        "normal",
        "low_voltage",
        "high_temperature",
        "light_failure"
    ])

    if fault_type == "normal":
        voltage = round(random.uniform(220, 240), 2)
        current = round(random.uniform(0.3, 1.5), 2)
        temperature = round(random.uniform(20, 55), 2)
        light_status = "ON"

    elif fault_type == "low_voltage":
        voltage = round(random.uniform(180, 214), 2)
        current = round(random.uniform(0.3, 1.5), 2)
        temperature = round(random.uniform(20, 55), 2)
        light_status = "ON"

    elif fault_type == "high_temperature":
        voltage = round(random.uniform(220, 240), 2)
        current = round(random.uniform(0.3, 1.5), 2)
        temperature = round(random.uniform(61, 85), 2)
        light_status = "ON"

    else:
        voltage = round(random.uniform(220, 240), 2)
        current = 0.0
        temperature = round(random.uniform(20, 55), 2)
        light_status = "OFF"

    return voltage, current, temperature, light_status


# Monitor five simulated streetlights
print("===== SMARTLIGHT AI AUTOMATED MONITOR =====")

report_file = "maintenance_report.csv"

with open(report_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "timestamp",
        "streetlight_id",
        "voltage",
        "current",
        "temperature",
        "light_status",
        "prediction"
    ])

    for number in range(1, 6):
        streetlight_id = f"SL-{number:03d}"

        voltage, current, temperature, light_status = (
            generate_sensor_readings()
        )

        readings = [[
            voltage,
            current,
            temperature,
            1 if light_status == "ON" else 0
        ]]

        prediction = int(model.predict(readings)[0])

        if prediction == 1:
            status = "POSSIBLE FAULT"
        else:
            status = "NO FAULT PREDICTED"

        print(f"\nStreetlight: {streetlight_id}")
        print(f"Voltage: {voltage} V")
        print(f"Current: {current} A")
        print(f"Temperature: {temperature} C")
        print(f"Light status: {light_status}")
        print(f"AI result: {status}")

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            streetlight_id,
            voltage,
            current,
            temperature,
            light_status,
            status
        ])

print("\nMonitoring simulation completed.")
print("Maintenance report saved:", report_file)
