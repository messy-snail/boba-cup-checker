import cv2

class color_finder:
    def __init__(self):
        self.result_string = 'nocup'
        pass
    def is_cup(self, frame, viz, write):
        hsv_color = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv_channels = cv2.split(hsv_color)
        normalized_hue = cv2.normalize(hsv_channels[0], None, 255, 0, cv2.NORM_MINMAX)
        normalized_sat = cv2.normalize(hsv_channels[1], None, 255, 0, cv2.NORM_MINMAX)
        normalized_val = cv2.normalize(hsv_channels[2], None, 255, 0, cv2.NORM_MINMAX)

        colorized_hue = cv2.applyColorMap(normalized_hue, cv2.COLORMAP_JET)
        colorized_sat = cv2.applyColorMap(normalized_sat, cv2.COLORMAP_JET)
        colorized_val = cv2.applyColorMap(normalized_val, cv2.COLORMAP_JET)

        if viz:

            cv2.imshow('hue', cv2.resize(colorized_hue, dsize=(320, 240), interpolation=cv2.INTER_AREA))
            cv2.imshow('sat', cv2.resize(colorized_sat, dsize=(320, 240), interpolation=cv2.INTER_AREA))
            cv2.imshow('val', cv2.resize(colorized_val, dsize=(320, 240), interpolation=cv2.INTER_AREA))

        if write:
            cv2.imwrite('hue.png', colorized_hue)
            cv2.imwrite('sat.png', colorized_sat)
            cv2.imwrite('val.png', colorized_val)

            cv2.imwrite('norm_hue.png', normalized_hue)
            cv2.imwrite('norm_sat.png', normalized_sat)
            cv2.imwrite('norm_val.png', normalized_val)

        self.result_string = 'nocup'

        self.result_string = 'cup'


        return self.result_string