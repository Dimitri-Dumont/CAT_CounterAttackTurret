from gpiozero import Servo
from time import sleep

# GPIO 23 (Pin 16)
# Set up with full range of motion (-1 to +1)
servo = Servo(23)

try:
    print("Starting continuous rotation")
    while True:
        # For continuous rotation, setting to max (1) 
        # will make it spin in one direction continuously
        servo.value = 1
        
        # No sleep needed between changes since we want constant motion
        # But we'll add a print statement so you know it's running
        print("Spinning... Press CTRL+C to stop")
        sleep(2)  # Just to prevent too many print statements

except KeyboardInterrupt:
    print("\nStopping servo")
    servo.value = 0  # Stop the rotation
    servo.detach()
