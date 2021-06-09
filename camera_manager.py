import cv2
import color_finder
import sys

class camera_manager:
    def __init__(self) -> None:
        self.cf = color_finder.color_finder()
        self.viz = False
        self.write = False
        self.left = 0
        self.right = 640
        self.top = 0
        self.bot = 480
        pass

    def Open(self):
        try:
            self.cap = cv2.VideoCapture(0)
        except Exception as e:
            print(e)
            print("cam connection error")
            return False
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0)
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        # self.cap.set(cv2.CAP_PROP_AUTO_FOCUS, 0)

        if not self.cap.isOpened():
            print('fail')
            return False
        return True

    def Run(self):
        while True:
            ret, self.frame = self.cap.read()

            if ret == False:
                print('cam read error1')
                break
            self.frame = self.frame[self.top:self.bot, self.left:self.right]
            number = cv2.countNonZero(self.frame[:,:,0])
            if number ==0:
                print('cam read error2')
                break

            # self.cf.is_cup(self.frame, viz, write)
            if self.viz:
                cv2.imshow('boba', self.frame)
            key = cv2.waitKey(60)
            if key == 27:
                break
        return True