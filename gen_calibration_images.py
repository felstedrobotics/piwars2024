import cv2
import time

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Unable to read camera feed")

is_ready = False
map = {
    0: "red",
    1: "green",
    2: "blue",
    3: "white",
    4: "grey",
}

for i in range(0, 5):
    # Capture first frame
    ret, frame = cap.read()
    if ret and not is_ready:
        # Save the image
        for x in range(0, 2):
            cv2.imwrite(f"./config/calibration_{map[i]}_{x+1}.jpg", frame)
    time.sleep(1)


# Release the VideoCapture object
cap.release()
