from picamera import PiCamera
from time import sleep

count = 0

# Define the GPIO pin for the button
button_pin = 2

# Create a camera object
camera = PiCamera()

# Function to capture an image
def capture_image():
    # Specify the file path and name for the image
    image_path = f"./images/image{count}.jpg"

    # Capture the image
    camera.capture(image_path)
    print("Image captured!")


# Keep the program running
while True:
    # Check for keypress: q
    if input() == 'q':
        count += 1
        capture_image(count)
    sleep(1)
