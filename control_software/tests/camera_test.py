from picamera2 import Picamera2
import time
from datetime import datetime

def test_camera():
    # Initialize the camera
    picam2 = Picamera2()
    
    # Configure the camera
    config = picam2.create_still_configuration()
    picam2.configure(config)
    
    # Start the camera
    picam2.start()
    
    # Wait for camera to warm up
    print("Warming up camera...")
    time.sleep(2)
    
    try:
        while True:
            # Generate timestamp for filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_image_{timestamp}.jpg"
            
            # Capture an image
            print(f"Capturing image: {filename}")
            picam2.capture_file(filename)
            
            # Ask if user wants to take another picture
            response = input("\nPress Enter to take another picture, or 'q' to quit: ")
            if response.lower() == 'q':
                break
                
    except KeyboardInterrupt:
        print("\nCamera test interrupted")
    finally:
        # Clean up
        picam2.close()
        print("Camera closed")

if __name__ == "__main__":
    test_camera()
