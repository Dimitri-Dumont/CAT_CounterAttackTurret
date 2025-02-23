#!/usr/bin/env python3

from picamera2 import Picamera2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Camera setup and capture
camera = Picamera2()
camera.start()
camera.capture_file("snapshot.jpg")
camera.stop()

# Email setup
sender_email = "dimitri3991@gmail.com"
sender_password = ""  # Replace with App Password (see below)
receiver_email = "dimitri3991@gmail.com"

msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = "Pi 5 Snapshot"

# Attach the image
with open("snapshot.jpg", "rb") as f:
    img = MIMEImage(f.read())
    msg.attach(img)

# Send email via Gmail SMTP
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)

print("Email sent!")
