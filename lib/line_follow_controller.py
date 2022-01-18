import sys
sys.path.append(r'/home/ryan/picar-x/lib')
from interpreter import interpreter
from sensing import sensing
import numpy as np
import time
from picarx_improved import Picarx

from utils import reset_mcu
reset_mcu()

class line_follow_controller(object):
    def __init__(self,scaling=80):
        self.scaling=scaling
        
    def control(self,px,direction):
        angle = direction * self.scaling
        px.set_dir_servo_angle(angle)
        return angle
    
if __name__ == '__main__':
    px = Picarx()
    brightness = float(input("Please enter brightness factor (0-1): "))
    polarity = int(input("Please enter polarity (1=light, -1=dark): "))
    sensor = sensing()
    processor = interpreter(brightness,polarity)
    controller = line_follow_controller()
    while True:
        adc_list = sensor.get_sensing_data()
        print(f"READING: {adc_list}")
        direction = processor.processing(adc_list)
        set_angle = controller.control(px,direction)
        print(f"Angle: {set_angle}")
        time.sleep(0.25)