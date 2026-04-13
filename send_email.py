# AUTHOR: Leo Li
# DATE: 2026/4/13

import smtplib
from email.message import EmailMessage

# Set the from and to email addresses and password
from_email_address = "1520087861@qq.com"
from_email_password = "xnwpqldbsshzifdg"
to_email_address = "2907517155@qq.com"

# Create a message object
msg = EmailMessage()

# Set the email body
body = "Hello from Leo using the Python Script!"
msg.set_content(body)

# Set sender and recipient 
msg["From"] = from_email_address
msg["To"] = to_email_address

# Set the email subject
msg["Subject"] = "TEST EMAIL"

# Connecting to the sever and sending email
# Edit with the provider's SMTP server and port
server = smtplib.SMTP("smtp.qq.com", 587)

# Start TLS for security
server.starttls()

# Login to the SMTP server, using the sender's email address and password
server.login(from_email_address, from_email_password)

# Send the message
server.send_message(msg)

print("<Email sent successfully>")

# Disconnect from the server
server.quit()