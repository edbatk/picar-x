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

class ultrasonic_controller(object):
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
    def __init__(self,picarx):
        """
        Parameters
        ----------
        px : Picarx
            picar object
        scaling : float
            scaling factor to increase motor movements
        
        """    
        self.px = picarx
        
    def control(self,command,direction):
        """
        Set motor speed and direction based on
        interpreted sensor direction
        """
        # print("Controlling")
        if command == 1:
            self.px.stop()
        elif command == -1:
            speed = -40*abs(direction) + 50
            self.px.forward(speed)
        return speed
    
    def consumer(self,message_bus,delay):
        """
        Read message from data bus
        """
        while True:
            # print("CONSUMING")
            message = message_bus.read()
            self.control(message)
            time.sleep(delay)
    
# if __name__ == '__main__':
#     px = Picarx()
#     brightness = float(input("Please enter brightness factor (0-1): "))
#     polarity = int(input("Please enter polarity (1=light, -1=dark): "))
#     sensor = sensing()
#     processor = interpreter(brightness,polarity)
#     controller = line_follow_controller(px)
#     while True:
#         adc_list = sensor.get_sensing_data()
#         print(f"READING: {adc_list}")
#         print('HERE')
#         direction = processor.processing(adc_list)
#         set_angle = controller.control(px,direction)
#         print(f"Angle: {set_angle}")
#         time.sleep(0.25)