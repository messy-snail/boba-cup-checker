import cv2
import numpy as np

class color_finder:
    def __init__(self):
        self.result_string = 'nocup'
        self.reference = None
        self.threshold_val = 30
        self.bin_counter = 100
        self.open_iteration = 2
        pass
    def is_cup(self, frame, viz, write):
        input_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        input_hsv_channels = cv2.split(input_hsv)

        reference_hsv = cv2.cvtColor(self.reference, cv2.COLOR_BGR2HSV)
        reference_hsv_channels = cv2.split(reference_hsv)

        subtraction_hue = cv2.subtract(reference_hsv_channels[0], input_hsv_channels[0])
        # subtraction_sat = cv2.subtract(reference_hsv_channels[1], input_hsv_channels[1])
        # subtraction_val = cv2.subtract(reference_hsv_channels[2], input_hsv_channels[2])

        _, binary_hue = cv2.threshold(subtraction_hue, self.threshold_val, 255, 0, cv2.THRESH_BINARY)

        # def morphologyEx(src, op, kernel, dst=None, anchor=None, iterations=None, borderType=None, borderValue=None): # real signature unknown; restored from __doc__
        opening_hue = cv2.morphologyEx(binary_hue, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8),
                                       iterations=self.open_iteration)
        counter = cv2.countNonZero(opening_hue)
        print(counter)
        if counter < self.bin_counter:
            self.result_string = 'nocup'
        else:
            self.result_string = 'cup'


        if viz:
            colorized_hue = cv2.applyColorMap(input_hsv_channels[0], cv2.COLORMAP_JET)
            colorized_sat = cv2.applyColorMap(input_hsv_channels[1], cv2.COLORMAP_JET)
            colorized_val = cv2.applyColorMap(input_hsv_channels[2], cv2.COLORMAP_JET)
            # cv2.imshow('hue', cv2.resize(colorized_hue, dsize=(320, 240), interpolation=cv2.INTER_AREA))
            # cv2.imshow('sat', cv2.resize(colorized_sat, dsize=(320, 240), interpolation=cv2.INTER_AREA))
            # cv2.imshow('val', cv2.resize(colorized_val, dsize=(320, 240), interpolation=cv2.INTER_AREA))

        if write:
            if viz:
                cv2.imwrite('hue.png', colorized_hue)
                cv2.imwrite('sat.png', colorized_sat)
                cv2.imwrite('val.png', colorized_val)
            cv2.imwrite('norm_hue.png', input_hsv_channels[0])
            cv2.imwrite('norm_sat.png', input_hsv_channels[1])
            cv2.imwrite('norm_val.png', input_hsv_channels[2])

        return self.result_string