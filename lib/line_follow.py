import sys
sys.path.append(r'/home/ryan/picar-x/lib')
from utils import reset_mcu
reset_mcu()
import time

from sensing import sensing
from interpreter import interpreter
from line_follow_controller import line_follow_controller
from picarx_improved import Picarx

if __name__=='__main__':
    px = Picarx()
    scaling = int(input("Please enter scaling (default 80): "))
    brightness = float(input("Please enter brightness factor (0-1): "))
    polarity = int(input("Please enter polarity (1=light, -1=dark): "))
    # min_speed = float(input("Please enter minimum speed: "))
    # max_speed = float(input("Please enter max speed: "))
    sensor = sensing()
    interpreter = interpreter(brightness, polarity)
    controller = line_follow_controller(scaling)
      
    while True:
        adc_list = sensor.get_sensing_data()
        direction = interpreter.processing(adc_list)
        set_angle = controller.control(px,direction)
        # speed = (max_speed - min_speed)*(abs(direction)-1.0)/-0.1
        speed = 0.5
        # px.forward(speed)
        time.sleep(0.1)
        
            