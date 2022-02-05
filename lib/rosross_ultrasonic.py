import sys
sys.path.append(r'/home/ryan/picar-x/lib')
from utils import reset_mcu
reset_mcu()
import time

from sensing import sensing
from interpreter import interpreter
from line_follow_controller import line_follow_controller
from ultrasonic_sensor import ultrasonic_sensing
from ultrasonic_interpreter import ultrasonic_interpreter
from ultrasonic_controller import ultrasonic_controller
from picarx_improved import Picarx
from pin import Pin

import concurrent.futures
from data_bus import message_bus

from rossros import Bus, ConsumerProducer, Producer, Consumer, Timer, Printer

if __name__=='__main__':
    # pin class trig D2, echo D3
    trig = Pin("D2")
    echo = Pin("D3")
    
    px = Picarx()
    scaling = int(input("Please enter scaling (default 80): "))
    brightness = float(input("Please enter brightness factor (0-1): "))
    polarity = int(input("Please enter polarity (1=light, -1=dark): "))
    
    sensor_bus = Bus([1, 1, 1], 'Sensor Bus')
    interpreter_bus = Bus(0, 'Interpreter Bus')
    termination_bus = Bus(0, 'Termination Bus')
    ultra_sensor_bus = Bus(0, 'Ultra Sensor Bus')
    ultra_interpreter_bus = Bus(0, 'Ultra Interpreter Bus')
    
    sensor = sensing()
    interpretor = interpreter(brightness,polarity)
    controller = line_follow_controller(px,scaling,'ultra')
    ultra_sensor = ultrasonic_sensing(trig, echo)
    ultra_interpreter = ultrasonic_interpreter(0.25)
    ultra_controller = ultrasonic_controller(px)
    
    s_delay = 0.01 # [s]
    i_delay = 0.01 # [s]
    c_delay = 0.01 # [s]
    us_delay = 0.01 # [s]
    ui_delay = 0.01 # [s]
    uc_delay = 0.01 # [s]
    t_delay = 0.01 # [s]
    
    wrapped_sensor = Producer(sensor.get_sensing_data,sensor_bus,s_delay,termination_bus,'sensor')
    wrapped_interpreter = ConsumerProducer(interpretor.processing,sensor_bus,interpreter_bus,i_delay,termination_bus,'interpreter')
    wrapped_controller = Consumer(controller.control,interpreter_bus,c_delay,termination_bus,'controller')
    wrapped_ultra_sensor = Producer(ultra_sensor.read,ultra_sensor_bus,us_delay,termination_bus,'ultra sensor')
    wrapped_ultra_interpreter = ConsumerProducer(ultra_interpreter.processing,ultra_sensor_bus,ultra_interpreter_bus,ui_delay,termination_bus,'ultra interpreter')
    wrapped_ultra_controller = Consumer(ultra_controller.control, (ultra_interpreter_bus,interpreter_bus),uc_delay,termination_bus,'ultra controller')
    timer = Timer(termination_bus, 3, t_delay, termination_bus, 'termination timer')
    
     
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        eSensor = executor.submit(wrapped_sensor)
        eInterpretor = executor.submit(wrapped_interpreter)
        eController = executor.submit(wrapped_controller)
        eUltraSensor = executor.submit(wrapped_ultra_sensor)
        eUltraInterpreter = executor.submit(wrapped_ultra_interpreter)
        eUltraController = executor.submit(wrapped_ultra_controller)
        eTimer = executor.submit(timer)

    eSensor.result()
    eInterpretor.result()
    eController.result()
    eUltraSensor.result()
    eUltraInterpreter.result()
    eUltraController.result()
    eTimer.result()