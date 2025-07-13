import time
import grovepi
import paho.mqtt.client as mqtt
import csv
from datetime import datetime

from generate_problem import generate_problem_file
from run_planner import run_planner

# -------------------------------
# Sensor/Actuator Ports
# -------------------------------
PIR_SENSOR = 3       # D3
TEMP_HUM_SENSOR = 7  # D7
LIGHT_SENSOR = 2     # A2
SOUND_SENSOR = 1     # A1
LED = 4              # D4
BUZZER = 2           # D2

# -------------------------------
# MQTT Setup
# -------------------------------
MQTT_BROKER = "localhost"
TOPIC_PREFIX = "building/sensors/"

# -------------------------------
# GrovePi Setup
# -------------------------------
grovepi.pinMode(PIR_SENSOR, "INPUT")
grovepi.pinMode(LED, "OUTPUT")
grovepi.pinMode(BUZZER, "OUTPUT")

# -------------------------------
# CSV Logging Setup
# -------------------------------
LOG_FILE = "sensor_log.csv"
try:
    with open(LOG_FILE, "x", newline='') as f:
        csv.writer(f).writerow(["Timestamp", "Temp (C)", "Humidity (%)", "Light", "Sound", "Motion"])
except FileExistsError:
    pass

# -------------------------------
# MQTT Client
# -------------------------------
client = mqtt.Client(protocol=mqtt.MQTTv311)
client.connect(MQTT_BROKER, 1883, 60)

# -------------------------------
# Helper: Apply AI Decision
# -------------------------------
def apply_ai_decision(decision):
    if decision == "ON":
        grovepi.digitalWrite(LED, 1)
        grovepi.digitalWrite(BUZZER, 1)
        client.publish(TOPIC_PREFIX + "ai_decision", "ON")
        print("? LED & BUZZER turned ON")
    else:
        grovepi.digitalWrite(LED, 0)
        grovepi.digitalWrite(BUZZER, 0)
        client.publish(TOPIC_PREFIX + "ai_decision", "OFF")
        print("? LED & BUZZER turned OFF")
        time.sleep(0.05)  # tiny delay to let hardware settle
        grovepi.digitalWrite(LED, 0)  # ensure OFF
        grovepi.digitalWrite(BUZZER, 0)
        
# -------------------------------
# Main Loop
# -------------------------------
try:
    while True:
        try:
            # -----------------------
            # Sensor readings
            # -----------------------
            motion = grovepi.digitalRead(PIR_SENSOR)
            light = grovepi.analogRead(LIGHT_SENSOR)
            sound = grovepi.analogRead(SOUND_SENSOR)

            # Friend-style safe temp/humidity read
            reading = grovepi.dht(TEMP_HUM_SENSOR, 0)
            try:
                temp, hum = reading[0], reading[1]
                if temp is None or hum is None or temp != temp or hum != hum:
                    temp, hum = -1, -1
            except (TypeError, IndexError):
                temp, hum = -1, -1

            # -----------------------
            # Publish to MQTT
            # -----------------------
            client.publish(TOPIC_PREFIX + "motion", motion)
            client.publish(TOPIC_PREFIX + "temperature", temp)
            client.publish(TOPIC_PREFIX + "humidity", hum)
            client.publish(TOPIC_PREFIX + "light", light)
            client.publish(TOPIC_PREFIX + "sound", sound)

            # -----------------------
            # Log to CSV
            # -----------------------
            with open(LOG_FILE, mode='a', newline='') as f:
                csv.writer(f).writerow([datetime.now(), temp, hum, light, sound, motion])

            # -----------------------
            # AI Planning
            # -----------------------
            state = {
                "dark": light < 100,
                "motion_detected": motion,
                "sound_detected": sound > 30
            }
            generate_problem_file(state)
            plan = run_planner()

            if any("activate-safety" in step for step in plan):
                apply_ai_decision("ON")
                with open("ai_decision.txt", "w") as f:
                    f.write("ON")
            else:
                apply_ai_decision("OFF")
                with open("ai_decision.txt", "w") as f:
                    f.write("OFF")

            # -----------------------
            # Console Output
            # -----------------------
            print(f"TEMP: {temp:.1f}C | HUM: {hum:.1f}% | LIGHT: {light} | SOUND: {sound} | MOTION: {'Yes' if motion else 'No'}")

        except Exception as e:
            print(f"?? Sensor or loop error: {e}")

        time.sleep(1)

except KeyboardInterrupt:
    print("?? Shutting down system.")
    grovepi.digitalWrite(LED, 0)
    grovepi.digitalWrite(BUZZER, 0)
