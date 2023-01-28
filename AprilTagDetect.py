import cv2
import apriltag
import numpy as np

# Create an AprilTag detector object
detector = apriltag.Detector()

# Camera parameters
fx = 800  # Focal length in x-axis
fy = 800  # Focal length in y-axis
cx = 320  # Principal point x-coordinate
cy = 240  # Principal point y-coordinate

# Get the size of the marker
marker_size = 0.1  # marker size in meters

# Open the video stream
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Detect AprilTag markers in the image
    result = detector.detect(frame)

    # Get the position and distance of the markers
    for r in result:
        # Compute the transformation matrix
        T = apriltag.homography_to_pose(r.homography, fx, fy, cx, cy)

        # Extract the position and distance
        position = T[0:3, 3]
        distance = np.linalg.norm(position)

        # Draw the bounding boxes around the detected markers
        cv2.rectangle(frame, (r.x, r.y), (r.x + r.width,
                      r.y + r.height), (0, 255, 0), 2)
        # Draw position and distance on the image
        cv2.putText(frame, "Position: " + str(position), (r.x, r.y-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, "Distance: " + str(distance), (r.x, r.y-40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # Show the frame
    cv2.imshow("AprilTag Detection", frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream and close the window
cap.release()
cv2.destroyAllWindows()
