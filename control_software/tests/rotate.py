from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Set up the pigpio factory
factory = PiGPIOFactory()

# GPIO 23 (Pin 16) with pigpio factory
servo = Servo(23, pin_factory=factory)

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
