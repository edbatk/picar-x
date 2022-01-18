import interpreter
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
        
if __name__ == '__main__':
    while True:
        break
    
        