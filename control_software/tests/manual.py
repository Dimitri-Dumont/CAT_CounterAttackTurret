from gpiozero import Servo, OutputDevice
import sys
import termios
import tty

# GPIO Pins
SERVO_PIN = 23   # Servo on GPIO 23
PUMP_PIN = 12    # Water pump on GPIO 12 (Relay control)

# Initialize devices
servo = Servo(SERVO_PIN)
pump = OutputDevice(PUMP_PIN)

# Possible servo positions
positions = [-1, 0, 1]
current_index = 1  # Start at center (0)
pump_on = False    # Track pump state

def get_key():
    """Reads a single character from standard input without requiring Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

print("Use LEFT (←) and RIGHT (→) arrow keys to move the servo.")
print("Press 'w' to toggle the water pump.")
print("Press 'q' to quit.")

try:
    while True:
        key = get_key()
        
        if key == '\x1b':  # Detect arrow key sequences
            key += get_key() + get_key()
            if key == '\x1b[D':  # Left arrow
                if current_index > 0:
                    current_index -= 1
                    print(f"Moving to position {positions[current_index]}")
                    servo.value = positions[current_index]
            elif key == '\x1b[C':  # Right arrow
                if current_index < len(positions) - 1:
                    current_index += 1
                    print(f"Moving to position {positions[current_index]}")
                    servo.value = positions[current_index]
        
        elif key == 'w':  # Toggle water pump
            pump_on = not pump_on
            if pump_on:
                print("Turning pump ON")
                pump.on()
            else:
                print("Turning pump OFF")
                pump.off()

        elif key == 'q':  # Quit when 'q' is pressed
            print("\nStopping servo and pump, exiting.")
            break

except KeyboardInterrupt:
    print("\nStopping servo and pump.")

finally:
    servo.detach()
    pump.off()  # Ensure the pump is turned off when exiting
