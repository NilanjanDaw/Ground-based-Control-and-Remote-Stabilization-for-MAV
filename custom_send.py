from interface import interfacer
from drone_controller import Drone
import time

interface = interfacer()
interface._controller()
print interface

while True:
    Drone.pitch = 70
    time.sleep(1)
    Drone.pitch = -70
    time.sleep(1)
    Drone.roll = 70
    time.sleep(1)
    Drone.roll = -70
    time.sleep(1)