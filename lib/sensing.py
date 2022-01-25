import sys
sys.path.append(r'/home/ryan/picar-x/lib')
from adc import ADC
import time
from utils import reset_mcu
reset_mcu()
from data_bus import message_bus

class sensing(object):
    def __init__(self):
        self.chn_0 = ADC("A0")
        self.chn_1 = ADC("A1")
        self.chn_2 = ADC("A2")
        
    def get_sensing_data(self):
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())
        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list
    
    def producer(self,message_bus,delay):
        while True:
            data = self.get_sensing_data()
            message_bus.write(data)
            time.sleep(delay)
    
if __name__ =='__main__':
    sensor = sensing()
    while True:
        readings = sensor.get_sensing_data()
        print(f"Sensor Reading: {readings}")
        time.sleep(0.25)