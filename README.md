# Ground Based Control and Remote Stabilization for Mav

## Instructions
The python files in the folder does the following jobs:
1.	color_blob_2 -> detects gesture and sends command to drone_controller. <br>
2.	custom_send -> To send custom drone commands(for testing purposes)<br>
3.	data_plotter -> To plot the telemetry data values<br>
4.	dataset_generator -> To be used to generate the CNN dataset<br>
5. 	drone_controller -> Interface class to be used to send drone commands to the MAV<br>
6.	dynamic_template -> Implements the dynamic template matching algorithm<br>
7.	interface -> redundant class not currently used. Maybe used to initialize drone PC connection.<br>
8.	LK -> Implements the Lucas Kannade algorithm<br>
9.	log -> Class to acquire data logs from drone<br>
10.	ramp -> test class implements ramp<br>

To run the gesture based drone control system run color_blob_2.py
To modify flight parameters eg. thrust and thrust increase step look into the file drone_controller.
