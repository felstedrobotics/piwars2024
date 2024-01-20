import numpy as np
import cv2
from calibration_loader import load_calibration

# load calibration values
values = load_calibration()
red_lower_arr = values[0]
red_upper_arr = values[1]
green_lower_arr = values[2]
green_upper_arr = values[3]
blue_lower_arr = values[4]
blue_upper_arr = values[5]
white_lower_arr = values[6]
white_upper_arr = values[7]
grey_lower_arr = values[8]
grey_upper_arr = values[9]

# Capturing video through webcam
webcam = cv2.VideoCapture(0)

while 1:
    # read the video frame by frame
    _, imageFrame = webcam.read()

    # Convert the imageFrame to grayscale
    grayFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)

    # Convert the imageFrame to HSV color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color and define mask
    red_lower = np.array([red_lower_arr], np.uint8)
    red_upper = np.array([red_upper_arr], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    # Set range for green color and define mask
    green_lower = np.array([green_lower_arr], np.uint8)
    green_upper = np.array([green_upper_arr], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    # Set range for blue color and define mask
    blue_lower = np.array([blue_lower_arr], np.uint8)
    blue_upper = np.array([blue_upper_arr], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    # Set range for white color and define mask
    white_lower = np.array([white_lower_arr], np.uint8)
    white_upper = np.array([white_upper_arr], np.uint8)
    white_mask = cv2.inRange(hsvFrame, white_lower, white_upper)

    # Set range for grey color and define mask
    grey_lower = np.array([grey_lower_arr], np.uint8)
    grey_upper = np.array([grey_upper_arr], np.uint8)
    grey_mask = cv2.inRange(hsvFrame, grey_lower, grey_upper)

    # Morphological Transform, Dilation for each color and bitwise_and operator
    # between imageFrame and mask determines to detect only that particular color
    kernel = np.ones((5, 5), "uint8")

    # For red color
    red_mask = cv2.dilate(red_mask, kernel)
    res_red = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask)

    # For green color
    green_mask = cv2.dilate(green_mask, kernel)
    res_green = cv2.bitwise_and(imageFrame, imageFrame, mask=green_mask)

    # For blue color
    blue_mask = cv2.dilate(blue_mask, kernel)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame, mask=blue_mask)

    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(
        red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 400:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(
                imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2
            )

            # Calculate grayscale brightness of the selected area
            selected_area = grayFrame[y : y + h, x : x + w]
            brightness = np.mean(selected_area)

            cv2.putText(
                imageFrame,
                f"Red Colour (Brightness: {brightness:.2f})",
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),
            )

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(
        green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(
                imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2
            )

            # Calculate grayscale brightness of the selected area
            selected_area = grayFrame[y : y + h, x : x + w]
            brightness = np.mean(selected_area)

            cv2.putText(
                imageFrame,
                f"Green Colour (Brightness: {brightness:.2f})",
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
            )

    # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(
        blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(
                imageFrame, (x, y), (x + w, y + h), (255, 0, 0), 2
            )

            # Calculate grayscale brightness of the selected area
            selected_area = grayFrame[y : y + h, x : x + w]
            brightness = np.mean(selected_area)

            cv2.putText(
                imageFrame,
                f"Blue Colour (Brightness: {brightness:.2f})",
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (255, 0, 0),
            )

    # Dilate the grey mask to remove noise
    white_mask = cv2.dilate(grey_mask, kernel)

    # Find contours in the grey mask
    contours, hierarchy = cv2.findContours(
        grey_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)

            # Detect grey color
            selected_area = imageFrame[y : y + h, x : x + w]
            std_dev = np.std(selected_area)
            if (
                std_dev < 10
            ):  # threshold for standard deviation to consider color as grey
                cv2.putText(
                    imageFrame,
                    "Grey Colour",
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (255, 255, 255),
                )

    # For white color
    white_mask = cv2.dilate(white_mask, kernel)
    res_white = cv2.bitwise_and(imageFrame, imageFrame, mask=white_mask)

    # Creating contour to track white color
    contours, hierarchy = cv2.findContours(
        white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(
                imageFrame, (x, y), (x + w, y + h), (255, 255, 255), 2
            )

            cv2.putText(
                imageFrame,
                "White Colour",
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (255, 255, 255),
            )

    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        webcam.release()
        cv2.destroyAllWindows()
        break
