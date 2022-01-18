import sys
sys.path.append(r'/home/ryan/picar-x/lib')
from utils import reset_mcu
reset_mcu()

from sensing import sensing
from interpreter import interpreter
from line_follow_controller import line_follow_controller
from picarx_improved import Picarx

if __name__=='__main__':
    px = Picarx()
    scaling = int(input("Please enter scaling (default 80): "))
    polarity = int(input("Please enter polarity (1=light, -1=dark): "))
    min_speed = int(input("Please enter minimum speed: "))
    max_speed = int(input("Please enter max speed: "))
    sensor = sensing()
    interpreter = interpreter(0.0, polarity)
    controller = line_follow_controller(scaling)
      
    while True:
        adc_list = sensing.get_sensing_data()
        direction = interpreter.processing(adc_list)
        set_angle = controller.control(direction)
        speed = (max_speed - min_speed)*(abs(direction)-1.00001)/-0.00001
        px.forward(speed)
            