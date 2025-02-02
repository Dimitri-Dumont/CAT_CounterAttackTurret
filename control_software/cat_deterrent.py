from gpiozero import MotionSensor, Servo, OutputDevice
from picamera2 import Picamera2
import time

pir = MotionSensor(4)  # GPIO4 for PIR sensor
camera = Picamera2()
camera.start()

def capture_motion():
    while True:
        if pir.motion_detected:
            # Capture image
            array = camera.capture_array()
            # Pass to CNN model
            if is_cat(array):  # model function
                aim_and_spray()

# Pan and tilt servos
pan = Servo(17)   # GPIO17
tilt = Servo(18)  # GPIO18

def aim_position(pan_angle, tilt_angle):
    # Convert angles to servo values (-1 to 1)
    pan.value = pan_angle / 90.0
    tilt.value = tilt_angle / 90.0                

pump = OutputDevice(24)  # GPIO24 for relay

def spray():
    pump.on()
    time.sleep(0.5)  # Spray duration
    pump.off()

def aim_and_spray():
    # Move to target position
    aim_position(45, 30)  # Example angles
    time.sleep(0.5)      # Wait for servos
    spray()
    # Return to rest position
    aim_position(0, 0)    