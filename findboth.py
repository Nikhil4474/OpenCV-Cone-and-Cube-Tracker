import cv2
import numpy as np

# Load the video capture object
cap = cv2.VideoCapture(0)

# Initialize the contour objects
orange_cone = None
purple_cube = None

while True:
    # Capture the current frame
    ret, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of orange color in HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Threshold the frame to get only orange colors
    mask_orange = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Find the contours in the frame
    # contours, _ = cv2.findContours(
    #     mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) doesn't work anymore in latest versions
    (_, contours, _) = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest orange contour
    if len(contours) > 0:
        orange_cone = max(contours, key=cv2.contourArea)

        # Compute the center of the orange contour
        M = cv2.moments(orange_cone)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        # Draw the orange contour and center on the frame
        cv2.drawContours(frame, [orange_cone], -1, (0, 255, 0), 2)
        cv2.circle(frame, (cX, cY), 7, (255, 0, 0), -1)
        cv2.putText(frame, "orange center", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Compute the angle of the orange cone in relation to the camera
        orange_angle = np.arctan2(
            cX - frame.shape[1]/2, frame.shape[0]) * 180 / np.pi
        
        # wait 100 ms before printing position and angleq
        cv2.waitKey(100)
        print("Orange cone Angle: {:.2f} degrees, Position: ({}, {})".format(
            orange_angle, cX, cY))

    # Define the range of purple color in HSV
    lower_purple = np.array([125, 50, 50])
    upper_purple = np.array([165, 255, 255])

    # Threshold the frame to get only purple colors
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)

    # Find the contours in the frame
    # contours, _ = cv2.findContours(mask_purple, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) old, doesn't work anymore in latest versions
    (_, contours, _) = cv2.findContours(mask_purple, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find the largest purple contour
    if len(contours) > 0:
        purple_cube = max(contours, key=cv2.contourArea)

        # Approximate the purple contour to a rectangle
        rect = cv2.minAreaRect(purple_cube)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Draw the purple contour and rectangle on the frame
        cv2.drawContours(frame, [purple_cube], -1, (0, 255, 0), 2)
        cv2.drawContours(frame, [box], -1, (0, 0, 255), 2)

        # Compute the center of the rectangle
        M = cv2.moments(box)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        # Draw the center of the rectangle on the frame
        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(frame, "purple center", (cX - 20, cY - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Compute the angle of the purple cube in relation to the camera
        purple_angle = np.arctan2(cX - frame.shape[1]/2, frame.shape[0]) * 180 / np.pi
        
        # wait 100 ms before printing position and angle
        cv2.waitKey(100)
        print("Purple cube Angle: {:.2f} degrees, Position: ({}, {})".format(purple_angle, cX, cY))

    # Show the frame
    cv2.imshow("Frame", frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
