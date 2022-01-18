from sensing import sensing
import numpy as np
import time
from utils import reset_mcu
import sys
sys.path.append(r'/home/ryan/picar-x/lib')
reset_mcu()

class interpreter(object):
    def __init__(self,brightness=0.0,polarity=1):
        self.brightness = brightness
        self.polarity = polarity
            
    def processing(self, adc_list):
        normalize = [float(i)/max(adc_list) for i in adc_list]
        print(f"Normalized Readings: {normalize}")
        max_diff = max(normalize)-min(normalize)
        print(f'Max Diff: {max_diff}')
        if max_diff > self.brightness:
            # rel_dir = normalize[0]-normalize[2]
            # print("Relative Direction: "+str(rel_dir))
            if self.polarity == 1:
                error = (max(normalize)-np.mean(normalize))*(0.7)
            elif self.polarity == -1:
                error = (min(normalize)-np.mean(normalize))*(0.7)
            print("Error: "+str(error))
            # rel_dir_pol = rel_dir*error*self.polarity
            rel_dir_pol = max_diff*error*self.polarity
        else:
            rel_dir_pol = 0
            print('Continue Forward')
        print(f"Direction: {rel_dir_pol}")
        return rel_dir_pol

if __name__ == '__main__':
    brightness = float(input("Please enter brightness factor (0-1): "))
    polarity = int(input("Please enter polarity (1=light, -1=dark): "))
    sensor = sensing()
    processor = interpreter(brightness,polarity)
    while True:
        reading = sensor.get_sensing_data()
        relative = processor.processing(reading)
        print(f"Move Relative: {relative}")
        time.sleep(0.25)