import cv2
import numpy as np

frame = cv2.imread("coen.png")
cropped_img = frame[0:int(frame.shape[0]/2)]
lower_green = np.array([50,125,110])
upper_green = np.array([100,255,255])
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
frame_hsv = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
frame_inrange = cv2.inRange(frame_hsv, lower_yellow, upper_yellow)
(_, contours, _) = cv2.findContours(
    frame_inrange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    img = cv2.drawContours(frame, [c], 0, (0,255,255), 3)
cv2.imshow("Camera Stream", img)
cv2.waitKey(0)