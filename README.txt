The python files in the folder does the following jobs:
1.	color_blob_2 -> detects gesture and sends command to drone_controller
2.	custom_send -> To send custom drone commands(for testing purposes)
3.	data_plotter -> To plot the telemetry data values
4.	dataset_generator -> To be used to generate the CNN dataset
5. 	drone_controller -> Interface class to be used to send drone commands to the MAV
6.	dynamic_template -> Implements the dynamic template matching algorithm
7.	interface -> redundant class not currently used. Maybe used to initialize drone PC connection.
8.	LK -> Implements the Lucas Kannade algorithm
9.	log -> Class to acquire data logs from drone
10.	ramp -> test class implements ramp

To run the gesture based drone control system run color_blob_2.py
To modify flight parameters eg. thrust and thrust increase step look into the file drone_controller.
