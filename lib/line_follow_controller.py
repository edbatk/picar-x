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
    """
    A class that controls motors based upon
    interpreted sensor information
    
    ...
    
    Attributes
    ----------
    px : Picarx
        picar object
    scaling : float
        scaling factor to increase motor movements
    
    """
    def __init__(self,picarx,scaling=80,mode='normal'):
        """
        Parameters
        ----------
        px : Picarx
            picar object
        scaling : float
            scaling factor to increase motor movements
        
        """
        
        self.px = picarx
        self.scaling=scaling
        self.mode = mode
        
    def control(self,direction):
        """
        Set motor speed and direction based on
        interpreted sensor direction
        """
        # print("Controlling")
        angle = direction * self.scaling
        self.px.set_dir_servo_angle(angle)
        if self.mode == 'normal':
            speed = -40*abs(direction) + 50
            self.px.forward(speed)
        return direction
    
    def consumer(self,message_bus,delay):
        """
        Read message from data bus
        """
        while True:
            # print("CONSUMING")
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