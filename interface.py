from drone_controller import Drone
import time, os, sys
from threading import Thread

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")

import cflib
from cflib.crazyflie import Crazyflie

"""
    Initializer class to establish drone-radio data link
"""
class interfacer:

    def _controller(self):
        cflib.crtp.init_drivers(enable_debug_driver=False)
        # Scan for Crazyflies and use the first one found
        print "Scanning interfaces for Crazyflies..."
        available = cflib.crtp.scan_interfaces()
        print "Crazyflies found:"
        print available
        for i in available:
            print i[0]

        if len(available) > 0:
            print len(available) - 1
            # print(available[0][len(available) - 1])
            drone = Drone(available[len(available) - 1][0])
            while not drone.connected:
                time.sleep(0.5)
            print "Test Connection Done!!!"
            Thread(target=drone. _motor_control).start()
            Drone.thruster = 0
            print(drone.thruster)
            time.sleep(1)
            Drone.thruster = 1
            print(drone.thruster)
            time.sleep(1)
            Drone.thruster = -1
            print(drone.thruster)
            time.sleep(0.5)
        else:
            print "No drones found!!!!"