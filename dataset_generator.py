import cv2
import time

camera = cv2.VideoCapture(0)


def capture_positive():
    while True:
        _, frame = camera.read()
        cv2.imshow("Capture", frame)
        cv2.imwrite("F:\\datasets\\positive_data\\color_positive" + str(time.time()) + ".jpg", frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("F:\\datasets\\positive_data\\gray_positive" + str(time.time()) + ".jpg", frame)
        if cv2.waitKey(1) == 27:
                break


def capture_negative():
     while True:
        _, frame = camera.read()
        cv2.imshow("Capture", frame)
        cv2.imwrite("F:\\datasets\\negative_data\\color_negative" + str(time.time()) + ".jpg", frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("F:\\datasets\\negative_data\\gray_negative" + str(time.time()) + ".jpg", frame)
        if cv2.waitKey(1) == 27:
                break


# capture_positive()
capture_negative()