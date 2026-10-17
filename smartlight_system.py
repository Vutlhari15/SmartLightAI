
import random
from fault_detector import detect_fault

# Simulate sensor readings for one streetlight
streetlight_id = "SL-001"

voltage = round(random.uniform(200, 250), 2)
current = round(random.uniform(0, 1.5), 2)
temperature = round(random.uniform(20, 80), 2)
light_status = random.choice(["ON", "OFF"])

# Display sensor readings
print("===== SMARTLIGHT AI MONITORING SYSTEM =====")
print("Streetlight ID:", streetlight_id)
print("Voltage:", voltage, "V")
print("Current:", current, "A")
print("Temperature:", temperature, "°C")
print("Light Status:", light_status)

# Analyse the readings
faults = detect_fault(
    voltage,
    current,
    temperature,
    light_status
)

# Display the analysis
print("\n===== FAULT DETECTION RESULTS =====")

if faults:
    print("Status: POSSIBLE FAULT DETECTED")

    for fault in faults:
        print("-", fault)
else:
    print("Status: NO FAULT DETECTED")
