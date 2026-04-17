# AUTHOR: Leo Li
# DATE: 2026/4/13

# --- 1. Import Libraries ---

# Email Part
import smtplib
from email.message import EmailMessage

# Soil Sensor Part
import RPi.GPIO as GPIO
import time


# --- 2. Function Definition ---

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
    print("<Time: %d:00>" % (get_current_hour()))

    # Disconnect from the server
    server.quit()


# Function to report status everyday at regular intervals
def job():
    # Declare and initialize the varibles needed
    global channel
    is_dry = GPIO.input(channel)
    hour = get_current_hour()

    if is_dry:
        subject = "Soil Status Report"
        body = """
        ---------------------------------------------
                     Soil Status Report
        ---------------------------------------------
        [Time]\t\t<%d:00>\n
        [Status]\t<Dry>\n
        [Notice]\t<You need to water your plant now!>
        """ % (hour)
    else:
        subject = "Soil Status Report"
        body = """
        ----------------------------------------------
                     Soil Status Report
        ----------------------------------------------
        [Time]\t\t<%d:00>\n
        [Status]\t<Wet>\n
        [Notice]\t<Good! Your plant has enough water.>
        """ % (hour)

    send_email(subject, body)


# Function to get the current hour of time
def get_current_hour():
    # Seconds since epoch
    seconds = time.time()
    # Format the time
    results = time.localtime(seconds)
    # Get current hour (Chinese, Beijing)
    current_hour = results.tm_hour

    return current_hour


# --- 3. Configure Soil Sensor ---

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set pin 4 as input to read data from the sensor
channel = 4
GPIO.setup(channel, GPIO.IN)

# --- 4. The Main Program ---

# Set the address information
from_email = "1520087861@qq.com"
password = "xnwpqldbsshzifdg"
to_email = "2907517155@qq.com"

# Hours to get the status and send email
email_hours = [8, 12, 16, 20]
# A flag
last_sent_hour = -1

# Program Title
print("===================")
print(" Soil Sensor Email ")
print("===================")

# Introduction of the program
print("--------------")
print(" Introduction ")
print("--------------")
print("This is a program aimed to remind you")
print("of watering your plant according to the")
print("moisture content in the soil. It will")
print("send you emails in certain time everyday")
print("containing the soil status and the time.")

print("-----------")
print(" Main Part ")
print("-----------")
print("<Program has started>")

while True:
    # Do the job (send status email) when it is the specific time
    current_hour = get_current_hour()
    for hour in email_hours:
        if current_hour == hour and current_hour != last_sent_hour:
            last_sent_hour = current_hour
            job()
    time.sleep(60)