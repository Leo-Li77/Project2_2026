# AUTHOR: Leo Li
# DATE: 2026/4/13

# ---- 1. Import Libraries ----

# Email Part
import smtplib
from email.message import EmailMessage

# Soil Sensor Part
import RPi.GPIO as GPIO
import time


# ---- 2. Function Definition ----

# Function to set up the email server
def set_server(from_email, password):
    # Email server and port
    SMTP_SERVER = "smtp.qq.com"
    SMTP_PORT = 587

    # Set the email server and port
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    # Start TLS for security
    server.starttls()

    # Login to the SMTP server
    print("<Logging in to the email server...>")
    server.login(from_email, password)

    return server


# Function to send email
def send_email(subject, body):
    global from_email, password, to_email
    # Set up the email server
    server = set_server(from_email, password)

    # Create a message object
    msg = EmailMessage()
        
    # Set the email body
    msg.set_content(body)
        
    # Set sender and recipient 
    msg["From"] = from_email
    msg["To"] = to_email
        
    # Set the email subject
    msg["Subject"] = subject
    
    # Send the message
    server.send_message(msg)
    print("<Email sent successfully>")

    # Disconnect from the server
    server.quit()


# Function to report status everyday at regular intervals
def job():
    global channel
    is_wet = GPIO.input(channel)
    if is_wet:
        subject = "Soil Status Report: Dry"
        body = """The soil is currently dry.
        Watering is needed."""
    else:
        subject = "Soil Status Report: Wet"
        body = """The soil is currently wet.
        No watering needed."""

    send_email(subject, body)


# ---- 4. Configure Soil Sensor ----

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set pin 4 as input to read data from the sensor
channel = 4
GPIO.setup(channel, GPIO.IN)

# ---- 5. The Main Program ----

# Set the address information
from_email = "1520087861@qq.com"
password = "xnwpqldbsshzifdg"
to_email = "2907517155@qq.com"

while True:
    job()
    # The program will send you an email per 6 hours
    time.sleep(6 * 60 * 60)
