import cv2
import color_finder

class camera_manager:
    def __init__(self) -> None:
        self.cf = color_finder.color_finder()
        pass

    def Open(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0)
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        # self.cap.set(cv2.CAP_PROP_AUTO_FOCUS, 0)

        if not self.cap.isOpened():
            print('fail')

    def Run(self, viz, write):
        while True:
            _, self.frame = self.cap.read()

            # self.cf.is_cup(self.frame, viz, write)
            if viz:
                cv2.imshow('boba', self.frame)
            key = cv2.waitKey(60)
            if key == 27:
                break