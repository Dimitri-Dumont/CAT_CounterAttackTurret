from picamera2 import Picamera2
from gpiozero import Servo, OutputDevice
import tflite_runtime.interpreter as tflite
from PIL import Image
import io
import numpy as np
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from datetime import datetime
import os

class Relay(OutputDevice):
    def __init__(self, pin, active_high=True):
        super(Relay, self).__init__(pin, active_high=active_high)



class CATDeterrent:
    def __init__(self):
        # Email configuration
        self.sender_email = "dimitri3991@gmail.com"
        self.sender_password = "phgk spyi uetc btux"
        self.receiver_email = "dimitri3991@gmail.com"
        
        # Initialize camera with basic configuration
        self.camera = Picamera2()
        preview_config = self.camera.create_preview_configuration()
        self.camera.configure(preview_config)
        
        # Initialize servos
        self.servo = Servo(23)   # GPIO17

        # Create relay object on GPIO 12 (pin 32)
        self.pump = Relay(12)  # GPIO24
        
        # Load TFLite model
        self.interpreter = self.load_model()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.img_size = (160, 160)
        
        # Create directory for cat detections
        self.image_dir = "cat_detections"
        os.makedirs(self.image_dir, exist_ok=True)
        
        # Cleanup any old temporary files
        self.cleanup_temp_files()
    
    def cleanup_temp_files(self):
        """Clean up any temporary files from previous runs."""
        if os.path.exists("temp_capture.jpg"):
            os.remove("temp_capture.jpg")

    def load_model(self):
        """Load TFLite model."""
        try:
            # Try simple interpreter first
            interpreter = tflite.Interpreter(model_path="/home/dimi/w.tflite")
            interpreter.allocate_tensors()
            return interpreter
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            print("Please ensure the model is a valid TFLite model.")
            raise
    
    def capture_and_process(self):
        """Capture image and check for cat, managing storage efficiently."""
        # Capture to temporary file
        temp_path = "temp_capture.jpg"
        self.camera.capture_file(temp_path)
        
        # Load and process image for inference
        with Image.open(temp_path) as image:
            image = np.array(image)
            processed_image = self.process_image(image)
            
            # Run detection
            is_cat = self.detect_cat(processed_image)
            
            if is_cat:
                # If cat detected, move to permanent storage with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                final_path = os.path.join(self.image_dir, f"cat_detected_{timestamp}.jpg")
                os.rename(temp_path, final_path)
                return True, final_path, image
            else:
                # If no cat, delete temporary file
                os.remove(temp_path)
                return False, None, image
    
    # Then in your process_image method, replace tf operations with PIL:
    def process_image(self, image):
        """Preprocess image for model inference."""
        # Convert to PIL Image if it's not already
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)
        
        # Resize and convert to numpy array
        image = image.resize(self.img_size)
        image = np.array(image)
        
        # Normalize and add batch dimension
        image = image.astype(np.float32) / 255.0
        image = np.expand_dims(image, axis=0)
        return image
    
    def detect_cat(self, processed_image):
        """Run inference on processed image."""
        self.interpreter.set_tensor(self.input_details[0]['index'], processed_image)
        self.interpreter.invoke()
        prediction = self.interpreter.get_tensor(self.output_details[0]['index'])
        return float(prediction[0]) > 0.5
    
    def send_notification(self, image_path):
        """Send email notification with the detected cat image."""
        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = self.receiver_email
            msg["Subject"] = "CAT Alert: Counter-Attack Initiated!"
            
            text = "A cat has been detected and the counter-attack system has been activated!"
            msg.attach(MIMEText(text, "plain"))
            
            with open(image_path, "rb") as f:
                img = MIMEImage(f.read())
                img.add_header('Content-Disposition', 'attachment', 
                             filename=os.path.basename(image_path))
                msg.attach(img)
            
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print("Alert email sent successfully!")
            
        except Exception as e:
            print(f"Failed to send email notification: {str(e)}")
    
    def activate_deterrent(self):
        """Activate water pump for 3 seconds."""
        print("Cat detected! Activating deterrent...")
        self.pump.on()
        time.sleep(3)
        self.pump.off()
    
    def aim_turret(self):
        """Aim the turret at predefined position."""
        self.servo.value = -1  # Center position
        self.servo.value = 1
        self.servo.value = 0
        
    def manage_storage(self):
        """Clean up old detection images if storage gets too full."""
        try:
            # Keep only last 50 detections
            files = sorted(os.listdir(self.image_dir))
            if len(files) > 50:
                for old_file in files[:-50]:
                    os.remove(os.path.join(self.image_dir, old_file))
                print(f"Cleaned up {len(files) - 50} old detection images")
        except Exception as e:
            print(f"Storage management error: {str(e)}")
    
    def run(self):
        """Main loop for the CAT deterrent system."""
        print("Starting CAT deterrent system...")
        self.camera.start()
        
        try:
            while True:
                # Capture and process image, managing storage efficiently
                is_cat, image_path, _ = self.capture_and_process()
                
                if is_cat:
                    # Activate deterrent
                    self.aim_turret()
                    self.activate_deterrent()
                    
                    # Send notification
                    self.send_notification(image_path)
                    
                    # Manage storage
                    self.manage_storage()
                    
                    # Wait longer after detection
                    time.sleep(5)
                else:
                    # Normal wait between captures
                    time.sleep(2)
                
        except KeyboardInterrupt:
            print("\nStopping CAT deterrent system...")
        finally:
            self.camera.stop()
            self.servo.detach()
            self.pump.off()
            self.cleanup_temp_files()
            print("System shutdown complete")

if __name__ == "__main__":
    deterrent = CATDeterrent()
    deterrent.run()