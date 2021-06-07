import sys
import cv2

class camera_manager:
    def __init__(self) -> None:
        pass

    def Open(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print('fail')

    def Run(self):
        while True:
            _, frame = self.cap.read()
            cv2.imshow('test', frame)
            key = cv2.waitKey(60)
            if key == 27:
                break