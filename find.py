import cv2
import numpy as np

# Load the video capture object
cap = cv2.VideoCapture("Coen.mp4")

while True:
    # Capture the current frame
    ret, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of orange color in HSV
    # lower_orange = np.array([5, 50, 50])
    # upper_orange = np.array([15, 255, 255])

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
       
    lower_purple = np.array([125, 50, 50])
    upper_purple = np.array([165, 255, 255])
    
    # Possible color values of purple (81,8,126) to 128, 0, 128
    # Value in OnShape (192,0,192)

    # Threshold the frame to get only orange colors
    # mask = cv2.inRange(hsv, lower_orange, upper_orange)
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    # mask = cv2.inRange(hsv, lower_purple, upper_purple)

    # Find the contours in the frame
    # contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    (_, contours, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)

        # Compute the center of the contour
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        # Draw the contour and center on the frame
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(frame, "center", (cX - 20, cY - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Compute the angle of the cone in relation to the camera
        angle = np.arctan2(cX - frame.shape[1]/2, frame.shape[0]) * 180 / np.pi

        # Print the angle and position of the cone
        cv2.waitKey(100)
        print("Angle: {:.2f} degrees, Position: ({}, {})".format(angle, cX, cY))

    # Show the frame
    cv2.imshow("Frame", frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
