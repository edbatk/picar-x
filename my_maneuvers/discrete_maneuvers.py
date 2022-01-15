import sys
sys.path.append(r'/home/ryan/picar-x/lib')
sys.path.append(r'/home/ryan/Documents/picar-x/lib')
from utils import reset_mcu
reset_mcu()

from picarx_improved import Picarx
import time

def linear_movements(px, speed, angle, duration):
    px.stop()
    px.set_dir_servo_angle(angle)
    time.sleep(0.5)
    if speed >= 0:
        px.forward(speed)
    else:
        px.backward(-speed)
    time.sleep(duration)
    px.stop()
    
def parallel_park(px, side):
    time.sleep(1.0)
    px.set_dir_servo_angle(0)
    if side == 'left':
        linear_movements(px, -7.5, -25, 0.75)
        linear_movements(px, -7.5, 25, 0.9)
        linear_movements(px, 7.5, 0, 1.0)
    elif side == 'right':
        linear_movements(px, -7.5, 25, 0.75)
        linear_movements(px, -7.5, -25, 0.9)
        linear_movements(px, 7.5, 0, 1.0)
        
def k_turn(px, side):
    time.sleep(1.0)
    px.set_dir_servo_angle(0)
    if side == 'left':
        linear_movements(px, 7.5, 25, 1.25)
        linear_movements(px, -7.5, -25, 1.25)
        linear_movements(px, 7.5, 25, 1.5)
        px.set_dir_servo_angle(0)
        linear_movements(px, 7.5, 0, 1.0)
    if side == 'right':
        linear_movements(px, -7.5, 25, 1.25)
        linear_movements(px, 7.5, -25, 1.25)
        linear_movements(px, 7.5, -25, 1.5)
        px.set_dir_servo_angle(0)
        linear_movements(px, 7.5, 0, 1.0)
        
        
if __name__ == "__main__":
    px = Picarx()
    curr_move = 'None'
    disc_maneuvers = ['linear', 'parallel-park', 'k-turn', 'end']
    sides = ['left', 'right']
    while curr_move != 'end':
        curr_move = input('Please select a maneuver from: [linear, parallel-park, k-turn, or end] ').lower()
        print(f'selected: {curr_move}')
        while curr_move not in disc_maneuvers:
            curr_move = input('Please select a maneuver from the following options: [linear, parallel-park, k-turn, or end] ').lower()
        if curr_move == 'end':
            print('Ending control... Please stand by ')
            time.sleep(1.0)
            continue
        elif curr_move == 'linear':
            speed = float(input('Please enter a desired speed (-ve for backwards) '))
            angle = float(input('Please enter a desired turning angle '))
            duration = float(input('Please enter a desired duration '))
            linear_movements(px, speed, angle, duration)
        elif curr_move == 'parallel-park':
            side = input('Please enter the desired direction [left or right] ').lower()
            while side not in sides:
                side = input('Please enter the desired direction [left or right] ').lower()
            parallel_park(px, side)
        elif curr_move == 'k-turn':
            side = input('Please enter the desired direction [left or right] ').lower()
            while side not in sides:
                side = input('Please enter the desired direction [left or right] ').lower()
            k_turn(px, side)
    print('Goodbye!')
            