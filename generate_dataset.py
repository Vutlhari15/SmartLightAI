
import random
import csv

# SmartLight AI: Dataset Generator

number_of_records = 1000

with open("smartlight_dataset.csv", "w", newline="") as file:
    writer = csv.writer(file)

    # Create the dataset headings
    writer.writerow([
        "voltage",
        "current",
        "temperature",
        "light_status",
        "fault"
    ])

    # Generate simulated sensor readings
    for i in range(number_of_records):

        fault_type = random.choice([
            "Normal",
            "Normal",
            "Normal",
            "Low Voltage",
            "High Temperature",
            "Light Failure"
        ])

        if fault_type == "Normal":
            voltage = round(random.uniform(220, 240), 2)
            current = round(random.uniform(0.3, 1.5), 2)
            temperature = round(random.uniform(20, 55), 2)
            light_status = "ON"
            fault = 0

        elif fault_type == "Low Voltage":
            voltage = round(random.uniform(180, 214), 2)
            current = round(random.uniform(0.3, 1.5), 2)
            temperature = round(random.uniform(20, 55), 2)
            light_status = "ON"
            fault = 1

        elif fault_type == "High Temperature":
            voltage = round(random.uniform(220, 240), 2)
            current = round(random.uniform(0.3, 1.5), 2)
            temperature = round(random.uniform(61, 85), 2)
            light_status = "ON"
            fault = 1

        else:
            voltage = round(random.uniform(220, 240), 2)
            current = 0.0
            temperature = round(random.uniform(20, 55), 2)
            light_status = "OFF"
            fault = 1

        writer.writerow([
            voltage,
            current,
            temperature,
            light_status,
            fault
        ])

print("Dataset generated successfully!")
print("Total records:", number_of_records)
print("File created: smartlight_dataset.csv")
