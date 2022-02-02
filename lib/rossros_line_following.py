import sys
sys.path.append(r'/home/ryan/picar-x/lib')
from utils import reset_mcu
reset_mcu()
import time

from sensing import sensing
from interpreter import interpreter
from line_follow_controller import line_follow_controller
from picarx_improved import Picarx

import concurrent.futures
from data_bus import message_bus

from rossros import Bus, ConsumerProducer, Producer, Consumer, Timer, Printer

if __name__=='__main__':
    px = Picarx()
    scaling = int(input("Please enter scaling (default 80): "))
    brightness = float(input("Please enter brightness factor (0-1): "))
    polarity = int(input("Please enter polarity (1=light, -1=dark): "))
    
    sensor_bus = Bus([1, 1, 1], 'Sensor Bus')
    interpreter_bus = Bus(0, 'Interpreter Bus')
    termination_bus = Bus(0, 'Termination Bus')
    
    sensor = sensing()
    interpretor = interpreter(brightness,polarity)
    controller = line_follow_controller(px,scaling)
    
    s_delay = 0.01 # [s]
    i_delay = 0.01 # [s]
    c_delay = 0.01 # [s]
    t_delay = 0.01 # [s]
    
    wrapped_sensor = Producer(sensor.get_sensing_data,sensor_bus,s_delay,termination_bus,'sensor')
    wrapped_interpreter = ConsumerProducer(interpretor.processing,sensor_bus,interpreter_bus,i_delay,termination_bus,'interpreter')
    wrapped_controller = Consumer(controller.control,interpreter_bus,c_delay,termination_bus,'controller')
    timer = Timer(termination_bus, 5, t_delay, 'termination timer')
    
     
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        eSensor = executor.submit(wrapped_sensor)
        eInterpretor = executor.submit(wrapped_interpreter)
        eController = executor.submit(wrapped_controller)
        eTimer = executor.submit(timer)

    eSensor.result()
    eInterpretor.result()
    eController.result()
    eTimer.result()