import sys
sys.path.append(r'/home/ryan/picar-x/lib')
sys.path.append(r'/home/ryan/Documents/picar-x/lib')
from utils import reset_mcu
reset_mcu()

from picarx_improved import Picarx
import time

if __name__ == "__main__":
    try:
        px = Picarx()
        time.sleep(2.0)
        px.set_dir_servo_angle(-5)
        time.sleep(3.0)
        px.forward(25)
        time.sleep(3.0)
        
    finally:
        px.forward(0)