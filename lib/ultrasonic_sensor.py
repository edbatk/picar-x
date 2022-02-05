import sys
sys.path.append(r'/home/ryan/picar-x/lib')
from adc import ADC
import time
from utils import reset_mcu
reset_mcu()
from data_bus import message_bus

class ultrasonic_sensing(object):
    """
    A class for ultrasonic sensor readings
    
    ...
    
    Attributes
    ----------
    channels : optional
        3 sensor channels form left to right 
    
    """
        
    def __init__(self, trig, echo, timeout=0.02):
        self.trig = trig
        self.echo = echo
        self.timeout = timeout
        
    def _read(self):
        self.trig.low()
        time.sleep(0.01)
        self.trig.high()
        time.sleep(0.00001)
        self.trig.low()
        pulse_end = 0
        pulse_start = 0
        timeout_start = time.time()
        while self.echo.value()==0:
            pulse_start = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1
        while self.echo.value()==1:
            pulse_end = time.time()
            if pulse_end - timeout_start > self.timeout:
                return -1
        during = pulse_end - pulse_start
        cm = round(during * 340 / 2 * 100, 2)
        return cm

    def read(self, times=10):
        for i in range(times):
            a = self._read()
            if a != -1 or a <= 300:
                return a
        return -1
    
    def producer(self,message_bus,delay):
        """
        Method that writes sesnor data to message_bus
        on a delay timer
        """
        while True:
            # print("PRODUCING")
            data = self.read()
            message_bus.write(data)
            time.sleep(delay)
    
# if __name__ =='__main__':
#     sensor = sensing()
#     while True:
#         readings = sensor.get_sensing_data()
#         print(f"Sensor Reading: {readings}")
#         time.sleep(0.25)