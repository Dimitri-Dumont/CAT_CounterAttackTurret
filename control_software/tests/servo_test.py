from gpiozero import Servo
import sys
import termios
import tty

# GPIO 23 (Pin 16)
servo = Servo(23)

# Possible servo positions
positions = [-1, 0, 1]
current_index = 1  # Start at center (0)

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

print("Use LEFT (←) and RIGHT (→) arrow keys to move the servo. Press 'q' to quit.")

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
        
        elif key == 'q':  # Quit when 'q' is pressed
            print("\nStopping servo and exiting.")
            break

except KeyboardInterrupt:
    print("\nStopping servo")

finally:
    servo.detach()
