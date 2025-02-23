from gpiozero import OutputDevice
from time import sleep

class Relay(OutputDevice):
    def __init__(self, pin, active_high=True):
        super(Relay, self).__init__(pin, active_high=active_high)

# Create relay object on GPIO 12 (pin 32)
pump_relay = Relay(12)

try:
    while True:
        print("Turning pump ON")
        pump_relay.on()
        sleep(1)  # Run for 1 second
        
        print("Turning pump OFF")
        pump_relay.off()
        sleep(5)  # Wait 2 seconds before next cycle
        
        # Ask if user wants to continue
        response = input("Press Enter to run again, or 'q' to quit: ")
        if response.lower() == 'q':
            break

except KeyboardInterrupt:
    print("\nStopping pump")
finally:
    pump_relay.off()  # Make sure pump is off when exiting
