from sensing import sensing
import numpy as np
import time
from utils import reset_mcu
import sys
sys.path.append(r'/home/ryan/picar-x/lib')
reset_mcu()
from data_bus import message_bus
import concurrent.futures

class ultrasonic_interpreter(object):
    """
    A class for interpretating of sensor readings
    that converts to useable directional headings
    based upon line following
    
    ...
    
    Attributes
    ----------
    brightness : float (0.0-1.0)
        scaling for sensitivity of sensor readings
    polarity : int (-1 or 1)
        checking against light or dark background
    
    """
    def __init__(self,threshold=0.25):
        """
        Parameters
        ----------
        brightness : float (0.0-1.0)
            scaling for sensitivity of sensor readings
        polarity : int (-1 or 1)
            checking against light or dark background
      
        """
        self.threshold = threshold
            
    def processing(self, distance):
        """
        Method for processing sensor information, returns
        direction of heading
        """
        if distance >= self.threshold:
            return -1
        elif distance < self.threshold:
            return 1
        
    
    def consumer_producer(self,in_bus,out_bus,delay): 
        """
        Method for writing to and reading from buses
        """
        while True:
            # print("CONSUMING PRODUCING")
            sensor_info = in_bus.read()
            process = self.processing(sensor_info)
            out_bus.write(process)
            time.sleep(delay)

# if __name__ == '__main__':
#     brightness = float(input("Please enter brightness factor (0-1): "))
#     polarity = int(input("Please enter polarity (1=light, -1=dark): "))
#     sensor = sensing()
#     processor = interpreter(brightness,polarity)
#     while True:
#         reading = sensor.get_sensing_data()
#         relative = processor.processing(reading)
#         print(f"Move Relative: {relative}")
#         time.sleep(0.25)