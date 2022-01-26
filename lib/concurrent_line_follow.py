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

if __name__=='__main__':
    px = Picarx()
    scaling = int(input("Please enter scaling (default 80): "))
    brightness = float(input("Please enter brightness factor (0-1): "))
    polarity = int(input("Please enter polarity (1=light, -1=dark): "))
    
    sensor = sensing()
    interpreter = interpreter(brightness, polarity)
    controller = line_follow_controller(px,scaling)
    sensor_bus = message_bus()
    interpreter_bus = message_bus()
     
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        eSensor = executor.submit(sensor.producer, sensor_bus, 0.01)
        eInterpretor = executor.submit(interpreter.consumer_producer, sensor_bus,interpreter_bus, 0.01)
        eController = executor.submit(controller.consumer, interpreter_bus, 0.01)

    eSensor.result()
    eInterpretor.result()
    eController.result()