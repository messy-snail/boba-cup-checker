import sys
import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('fail')

while True:
    _, frame = cap.read()
    cv2.imshow('test', frame)
    key = cv2.waitKey(60)
    if key == 27:
        break