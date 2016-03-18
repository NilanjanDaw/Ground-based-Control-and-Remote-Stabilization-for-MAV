import cv2
import numpy as np
from interface import interfacer
from drone_controller import Drone

camera = cv2.VideoCapture(0)

threshold = 20
fontFace = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fontScale = 1
thickness = 1
old_x, old_y = 0, 0


def findDirection(frame, x, old_x, y, old_y):
    diff_x = old_x - x
    diff_y = old_y - y
    co_x = 0
    control = 0
    # cv2.putText(frame, str(diff_x) + " " + str(diff_y), (x, y), fontFace, fontScale, (0, 0, 255),thickness)
    if abs(diff_x) > 10 or abs(diff_y) > 10:
        if abs(diff_x) > abs(diff_y):
            if diff_x > 0:
                cv2.putText(frame, "Left", (co_x, y), fontFace, fontScale, (0, 0, 255), thickness)
                control = 50
            else:
                cv2.putText(frame, "right", (co_x, y), fontFace, fontScale, (0, 0, 255), thickness)
                control = -50
            Drone.pitch = control
        else:
            if diff_y > 0:
                cv2.putText(frame, "up", (co_x, y), fontFace, fontScale, (0, 0, 255), thickness)
                control = -50
            else:
                cv2.putText(frame, "down", (co_x, y), fontFace, fontScale, (0, 0, 255), thickness)
                control = 50
            Drone.roll = control
    print x
    return x


def tracker(frame2, ThresholdImage):
    global old_x, old_y
    contours, hierarchy = cv2.findContours(ThresholdImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    area_max = -1
    if len(contours) > 0:
        contour_max = contours[0]
        for cnt in contours:
            # print hierarchy.shape," ", hierarchy[0][i]
            area = cv2.contourArea(cnt)
            if area_max < area:
                contour_max = cnt
                area_max = area
            i += 1
        x, y, w, h = cv2.boundingRect(contour_max)
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 0, 255), 0)
        print str(x) + " " + str(y)
        findDirection(frame2, x, old_x, y, old_y)
        old_x = x
        old_y = y
    cv2.imshow("Tracked", frame2)
    return 0


def detector():
    while 1:
        _, frame1 = camera.read()
        grayScale1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

        _, frame2 = camera.read()
        grayScale2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        differenceImage = cv2.absdiff(grayScale1, grayScale2)

        _, ThreshImage = cv2.threshold(differenceImage, threshold, 255, cv2.THRESH_BINARY)
        ThreshImage = cv2.blur(ThreshImage, (5, 5), 0)
        kernel = np.ones((5, 5), np.uint8)
        ThreshImage = cv2.erode(ThreshImage, kernel, iterations=2)
        _, ThreshImage = cv2.threshold(ThreshImage, threshold, 255, cv2.THRESH_BINARY)
        tracker(frame2, ThreshImage)
        # cv2.imshow("Threshold", ThreshImage)
        # cv2.imshow("difference", differenceImage)
        if cv2.waitKey(1) == 27:
            break


if __name__ == '__main__':
    interface = interfacer()
    interface._controller()
    print interface

    detector()
    camera.release()
    cv2.destroyAllWindows()
