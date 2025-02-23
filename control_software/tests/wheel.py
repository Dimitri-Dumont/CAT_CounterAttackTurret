from gpiozero import Servo
from time import sleep

# Basic servo setup without pigpio for now
servo = Servo(23)

try:
    print("Starting continuous rotation")
    while True:
        servo.value = 1
        print("Spinning... Press CTRL+C to stop")
        sleep(2)
	
	
except KeyboardInterrupt:
    print("\nStopping servo")
    servo.value = 0
    servo.detach()
