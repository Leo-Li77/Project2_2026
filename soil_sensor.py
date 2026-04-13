# AUTHOR: Leo Li
# DATE: 2026/4/13

# ---- 1. Import and Configure ----
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

channel = 4    # Set pin 4 as input one to read data from the sensor
GPIO.setup(channel, GPIO.IN)

# ---- 2. Function Definition ----
def callback(channel):
    if GPIO.input(channel):
        print("Water Detected!")
    else:
        print("Water Detected!")

# ---- 3. Event Detection ----
# Let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime = 300)
# Assign function to GPIO PIN, Run function on change
GPIO.add_event_callback(channel, callback)

# ---- 4. Infinite Loop ----
while True:
    time.sleep(0)
