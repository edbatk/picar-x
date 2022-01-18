import sensing
from sensing import get_sensing_data
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
        max_diff = max(normalize)-min(normalize)
        if max_diff > self.sensitivity:
            rel_dir = normalize[0]-normalize[2]
            print("Relative Direction: "+str(rel_dir))
            if self.polarity == 1:
                error = (max(normalize)-np.mean(normalize))*(2/3)
            elif self.polarity == -1:
                error = (min(normalize)-np.mean(normalize))*(2/3)
            print("Error: "+str(error))
            rel_dir_pol = rel_dir*error*self.polarity
        else:
            rel_dir_pol = 0

        return rel_dir_pol

        
if __name__ == '__main__':
    sens = sensing()
    interpretor = interpreter(0.0, -1)

    while True:
        break           