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
    time.sleep(1.0)
    if speed >= 0:
        px.forward(speed)
    else:
        px.backward(-speed)
    time.sleep(duration)
    px.stop()
    


if __name__ == "__main__":
    try:
        px = Picarx()
        time.sleep(1.0)
        linear_movements(px, 20, 0, 3.0)
        time.sleep(px, -20, 0, 2.0)
        time.sleep(1.0)
        linear_movements(px, 15, -25, 1.0)
        time.sleep(1.0)
        
        
    finally:
        px.forward(0)
        px.stop()