import sys
sys.path.append(r'/home/ryan/picar-x/lib')
from interpreter import interpreter
from sensing import sensing
import numpy as np
import time
from picarx_improved import Picarx
from utils import reset_mcu
reset_mcu()
from data_bus import message_bus

class line_follow_controller(object):
    def __init__(self,picarx,scaling=80):
        self.px = picarx
        self.scaling=scaling
        
    def control(self,direction):
        print("Controlling")
        angle = direction * self.scaling
        self.px.set_dir_servo_angle(angle)
        speed = -40*abs(direction) + 50
        self.px.forward(speed)
        return angle
    
    def consumer(self,message_bus,delay):
        while True:
            print("CONSUMING")
            message = message_bus.read()
            self.control(message)
            time.sleep(delay)
    
if __name__ == '__main__':
    px = Picarx()
    brightness = float(input("Please enter brightness factor (0-1): "))
    polarity = int(input("Please enter polarity (1=light, -1=dark): "))
    sensor = sensing()
    processor = interpreter(brightness,polarity)
    controller = line_follow_controller(px)
    while True:
        adc_list = sensor.get_sensing_data()
        print(f"READING: {adc_list}")
        print('HERE')
        direction = processor.processing(adc_list)
        set_angle = controller.control(px,direction)
        print(f"Angle: {set_angle}")
        time.sleep(0.25)