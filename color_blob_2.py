import cv2
import numpy as np
from interface import interfacer
from drone_controller import Drone
import time
import sys
'''
Author: Nilanjan Daw and Debapriya Paul
Date: December 21, 2015
Current Version: 1.10
Place: IIT Kharagpur
'''
'''
Overview:
    1.  Acquiring images through a webcam and using it to detect and decipher gestures
    2.  Using those gestures to control a "crazy" crazyflie 2.0 drone
'''

cap = cv2.VideoCapture(1) # Setting webcam for video capture
"""
    Typesetting variables
"""
fontFace = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fontScale = 1
thickness = 1
"""
    Threshold values and memory variables
"""
threshold = 20
threshold_area_value = 750
old_x, old_y = 0, 0
old_area = 0
"""
    Parameter(s): Array of contours
    Return: Returns the contour with the maximum area. If contour array is null returns an empty list
    Function: Finds the largest contour from a list of contours.
"""
def find_max_contour(contour_array):
    max_area = -1
    for cnt in contour_array:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_contour = cnt
    if len(contour_array) > 0:
        return max_contour
    else:
        return ()

"""
    Captures first frame and grayscales it
"""
_, prev = cap.read()
prev = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

"""
    For testing only
green = np.uint8([[[255, 0, 0]]])
hsv_green = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
print hsv_green
"""

"""
    Parameter(s): Old and new 1. X,Y coordinates amd 2. area of detected contour
    Return: Returns the direction of motion of the drone.
    Function: Determines the direction of motion and instructs drone control to take necessary actions
"""
def findDirection(x, old_x, y, old_y, new_area, old_area):
    diff_x = old_x - x
    diff_y = old_y - y
    diff_area = old_area - new_area
    x = 0
    # cv2.putText(frame, str(diff_x) + " " + str(diff_y), (x, y), fontFace, fontScale, (0, 0, 255),thickness)
    if abs(diff_area) > threshold_area_value:
        if diff_area > 0:
            cv2.putText(frame, "backward", (x, y), fontFace, fontScale, (0, 0, 255),thickness)
            x = -30 # angle of pitch
        else:
            cv2.putText(frame, "forward", (x, y), fontFace, fontScale, (0, 0, 255),thickness)
            x = 30
            Drone.pitch = x
    else:
        if abs(diff_x) > 10 or abs(diff_y) > 10:
            if abs(diff_x) > abs(diff_y):
                if diff_x > 0:
                    cv2.putText(frame, "Left", (x, y), fontFace, fontScale, (0, 0, 255),thickness)
                    x = -30 # angle of roll
                else:
                    cv2.putText(frame, "right", (x, y), fontFace, fontScale, (0, 0, 255),thickness)
                    x = 30
                Drone.roll = x
            else:
                if diff_y > 0:
                    cv2.putText(frame, "up", (x, y), fontFace, fontScale, (0, 0, 255),thickness)
                    x = 1 # thruster multiplier, thrust step can be changed in the drone_controller file
                else:
                    cv2.putText(frame, "down", (x, y), fontFace, fontScale, (0, 0, 255),thickness)
                    x = -1
                Drone.thruster = x
                Drone.thrust_flag = True
    # print x
    # cv2.imwrite("screenshot" + str(time.time()) + ".jpg", frame)
    return x
"""
    Initializes the communication link between the PC and the drone
    Look into python file interface.py for implementation
"""
interface = interfacer()
interface._controller()
print interface
"""
Main Loop to capture image and perform processing
"""
while 1:

    _, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Acquiring frames
    prev = frame_gray
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # porting acquired image into HSV color space

    lower_blue = np.array([100, 50, 50], dtype=np.uint8) # HSV lower and Upper value limits of tracked object
    upper_blue = np.array([140, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    res = cv2.bitwise_and(frame, frame, mask=mask) # setting mask on image

    res_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY) # converting image into gray scale
    _, ThreshImage = cv2.threshold(res_gray, threshold, 255, cv2.THRESH_BINARY)
    ThreshImage = cv2.blur(ThreshImage, (5, 5), 0)
    kernel = np.ones((5, 5), np.uint8)
    ThreshImage = cv2.erode(ThreshImage, kernel, iterations=2)
    _, res_gray = cv2.threshold(ThreshImage, threshold, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(res_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # finding contours in the image
    #cv2.imshow('frame', frame)
    cv2.imshow('res', res)
    max_contour = find_max_contour(contours) # Invoking max_contour() function to find the contour with maximum size
    if len(max_contour) < 1:
        continue
    x, y, w, h = cv2.boundingRect(max_contour) # finding coordinates of the returned contour
    new_area = cv2.contourArea(max_contour) # finding area of the contour
    thruster = findDirection(x, old_x, y, old_y, new_area, old_area) # invoking findDirection() method to get the direction of contour motion
    Drone.thruster = 1 if thruster > 0 else -1
    # print str(old_x) + " " + str(old_y) + " " + str(x) + " " + str(y)
    old_x = x
    old_y = y
    old_area = new_area
    text = str(x) + " " + str(y)
    cv2.putText(frame, text, (x, y), fontFace, fontScale, (0, 0, 255),thickness) # Drawing on the image
    cv2.drawContours(frame, max_contour, -1, (0, 255, 0), 3)
    epsilon = 0.1 * cv2.arcLength(max_contour, True)
    approx = cv2.approxPolyDP(max_contour, epsilon, True)
    cv2.imshow('contours', frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        sys.exit(0)
        break

cv2.destroyAllWindows()