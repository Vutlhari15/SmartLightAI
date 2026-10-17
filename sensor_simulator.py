
import random

# SmartLight AI: Simulated Streetlight Sensors

streetlight_id = "SL-001"

# Simulate sensor readings
voltage = round(random.uniform(215, 245), 2)
current = round(random.uniform(0.3, 1.5), 2)
temperature = round(random.uniform(20, 75), 2)

# Simulate whether the light is working
light_status = random.choice(["ON", "OFF"])

# Display the sensor data
print("===== SMARTLIGHT AI SENSOR DATA =====")
print("Streetlight ID:", streetlight_id)
print("Voltage:", voltage, "V")
print("Current:", current, "A")
print("Temperature:", temperature, "°C")
print("Light Status:", light_status)
