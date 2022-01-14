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
        linear_movements(px, -7.5, -25, 1.0)
        linear_movements(px, 7.5, 50, 0.25)
        linear_movements(px, 5, 0, 0.25)
    elif side == 'right':
        linear_movements(px, -7.5, 25, 1.0)
        linear_movements(px, 7.5, -50, 0.25)
        linear_movements(px, 5, 0, 0.25)
        
if __name__ == "__main__":
    try:
        px = Picarx()
        time.sleep(1.0)
        parallel_park(px,'left')
          
        
    finally:
        px.forward(0)
        px.stop()