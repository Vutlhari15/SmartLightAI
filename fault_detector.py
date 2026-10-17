
# SmartLight AI - Basic Fault Detection

def detect_fault(voltage, current, temperature, light_status):
    faults = []

    # Check the electrical voltage
    if voltage < 215 or voltage > 245:
        faults.append("Abnormal voltage detected")

    # Check whether current is flowing
    if light_status == "ON" and current < 0.1:
        faults.append("Possible current supply fault")

    # Check whether the equipment is overheating
    if temperature > 60:
        faults.append("High temperature detected")

    # Check whether the light is switched off
    if light_status == "OFF":
        faults.append("Streetlight is OFF")

    return faults


# Test using simulated sensor readings
streetlight_id = "SL-001"
voltage = 235.96
current = 0.91
temperature = 67.53
light_status = "OFF"

faults = detect_fault(
    voltage,
    current,
    temperature,
    light_status
)

print("===== SMARTLIGHT AI FAULT REPORT =====")
print("Streetlight ID:", streetlight_id)

if faults:
    print("Status: POSSIBLE FAULT DETECTED")

    for fault in faults:
        print("-", fault)
else:
    print("Status: NO FAULT DETECTED")
