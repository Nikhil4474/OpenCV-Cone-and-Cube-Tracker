# import cv2
# import numpy as np
# vid = cv2.VideoCapture('coen.mp4')
# lower_yellow = np.array([20,100,100])
# upper_yellow = np.array([30,255,255])
# vid_hsv = cv2.cvtColor(vid, cv2.COLOR_BGR2HSV)
# vid_inRange = cv2.inRange(vid_hsv, lower_yellow, upper_yellow)
# cv2.imshow("camera", vid_inRange)
# cv2.waitKey(0)

# Doesn't work, have to figure out why
# Error is TypeError: Expected Ptr<cv::UMat> for argument 'src' in line six
# assuming its something to do with converting the video to HSV because its not UMat
# I think Mat = matrix?



import cv2
import numpy as np
frame  = cv2.imread("out[ut.jpg")
# Doesn't competly work with cone, color is off
# frame = cv2.VideoCapture(0)  Doesn't work, have to figure out why
lower_green = np.array([50,125,110])
upper_green = np.array([100,255,255])
frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
frame_inrange = cv2.inRange(frame_hsv,lower_green,upper_green)
cv2.imshow("Camera stream", frame_inrange)
cv2.waitKey(0)


'''
This sort of works with cone

import cv2
import numpy as np
frame  = cv2.imread("coen.png")
lower_green = np.array([50,125,110])
upper_green = np.array([100,255,255])
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
frame_inrange = cv2.inRange(frame_hsv,lower_yellow,upper_yellow)
cv2.imshow("Camera stream", frame_inrange)
cv2.waitKey(0)
'''