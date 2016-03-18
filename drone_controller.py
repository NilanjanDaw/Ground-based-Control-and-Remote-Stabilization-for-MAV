import time, os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import cflib
import cflib.crtp
from cfclient.utils.logconfigreader import LogConfig
from cflib.crazyflie import Crazyflie

"""
    Controller class to control the Crazyflie 2.0 drone
"""


def drone_hover():
    pass


class Drone:
    thruster = 0
    yaw = 0
    pitch = 0
    roll = 0
    connected = False
    thrust_flag = False

    def __init__(self, link_uri):

        self._cf = Crazyflie()

        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        self._cf.open_link(link_uri)

        print "Connecting to %s" % link_uri

    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""

        # Start a separate thread to do the motor test.
        # Do not hijack the calling thread!
        # Thread(target=self._ramp_motors).start()
        print "connected to %s" % link_uri
        print("before Logconfig")
        Drone.connected = True

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)"""
        print "Connection to %s failed: %s" % (link_uri, msg)

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print "Connection to %s lost: %s" % (link_uri, msg)

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print "Disconnected from %s" % link_uri

    def _motor_control(self):
        print "Motor control started!!"
        base_thrust_value = 35000
        thrust_step = 8000
        thrust = base_thrust_value
        pitch_rate = 10
        roll_rate = 10
        yaw_rate = 0

        # win = pg.GraphicsWindow()
        # win.setWindowTitle('pyqtgraph example: Scrolling Plots')

        # Unlock startup thrust protection
        self._cf.commander.send_setpoint(0, 0, 0, 0)
        self._lg_stab = LogConfig(name="Stabilizer", period_in_ms=100)
        self._lg_stab.add_variable("stabilizer.thrust", "float")
        self._lg_stab.add_variable("stabilizer.roll", "float")
        self._lg_stab.add_variable("stabilizer.pitch", "float")
        self._lg_stab.add_variable("stabilizer.yaw", "float")

        # Adding the configuration cannot be done until a Crazyflie is
        # connected, since we need to check that the variables we
        # would like to log are in the TOC.
        try:
            self._cf.log.add_config(self._lg_stab)
            # This callback will receive the data
            self._lg_stab.data_received_cb.add_callback(self._stab_log_data)
            # This callback will be called on errors
            self._lg_stab.error_cb.add_callback(self._stab_log_error)
            # Start the logging
            self._lg_stab.start()
        except KeyError as e:
            print "Could not start log configuration," \
                  "{} not found in TOC".format(str(e))
        except AttributeError:
            print "Could not add Stabilizer log config, bad configuration."

        while True:
            self._cf.param.set_value("flightmode.althold", "True")

            self._cf.commander.send_setpoint(Drone.roll, Drone.pitch, Drone.yaw, thrust)
            # thrust = base_thrust_value
            # if self.thrust_flag:
            # self._cf.param.set_value("flightmode.althold", "False")
            """
            if thrust < 65000 and Drone.thruster == 1:
                thrust += thrust_step * Drone.thruster
                Drone.thruster = 0
            elif thrust + thrust_step * Drone.thruster > 35000 and Drone.thruster == -1:
                thrust += thrust_step * Drone.thruster
                Drone.thruster = 0
            """

            if 35000 < thrust + thrust_step * Drone.thruster <= 65000:
                thrust += thrust_step * Drone.thruster
                Drone.thruster = 0
            Drone.thruster = 0
            self.thrust_flag = False
            # else:
            # self._cf.param.set_value("flightmode.althold", "True")
            Drone.pitch = Drone.roll = 0
            # time.sleep(0.1)

        self._cf.commander.send_setpoint(0, 0, 0, 0)
        # Make sure that the last packet leaves before the link is closed
        # since the message queue is not flushed before closing
        time.sleep(0.1)
        self._cf.close_link()

    def _stab_log_error(self, logconf, msg):
        """Callback from the log API when an error occurs"""
        print "Error when logging %s: %s" % (logconf.name, msg)

    def _stab_log_data(self, timestamp, data, logconf):
        """Callback froma the log API when data arrives"""
        print "Log: [%d][%s]: %s" % (timestamp, logconf.name, data)
        print(data['stabilizer.roll'])

        self.roll = -data['stabilizer.roll']
        self.pitch = -data['stabilizer.pitch']
        self.yaw = -data['stabilizer.yaw']

        f_thrust = open('data_log_thrust.txt', 'a')
        f_roll = open('data_log_roll.txt', 'a')
        f_pitch = open('data_log_pitch.txt', 'a')
        f_yaw = open('data_log_yaw.txt', 'a')
        f_data = open('data_log.txt', 'a')
        f_thrust.write(str(data['stabilizer.thrust']) + ",")
        f_roll.write(str(data['stabilizer.roll']) + ",")
        f_pitch.write(str(data['stabilizer.pitch']) + ",")
        f_yaw.write(str(data['stabilizer.yaw']) + ",")
        f_data.write(
            str(data['stabilizer.thrust']) + "," + str(data['stabilizer.roll']) + "," + str(
                data['stabilizer.pitch']) + "," + str(data['stabilizer.yaw']) + "\n")
        f_roll.close()
        f_pitch.close()
        f_yaw.close()
        f_thrust.close()
        f_data.close()
