from behave import *
from math import inf
from subprocess import call
import os
import gps_takeoff
import laser_sub
	


############### Given: Hokuyo LIDAR rostopic is publishing ############ 
@given('TerraRanger One ROS node is running')
def teraranger_ros_node_running(nodeCheckScriptExitValue):
    nodeCheckScriptExitValue= os.system('sh /home/lowe/catkin_ws/src/arm_and_takeoff/BDDtest_python_controlDrone_and_groundDetection/src/features/steps/node_running_script.sh')
    assert nodeCheckScriptExitValue==0    


################ When drone altitude less than 0.2m ###################
@when('The drone is at an altitude less than 0.2 meters above ground level')
def drone_flying_lower_than_0dot2m (self):
    low_altitude_threshold= gps_takeoff.low_altitude_threshold
    drone_terranger_altitude =laser_sub.getscanLaser_altitude()
    assert drone_terranger_altitude < low_altitude_threshold

# Then altitude received from Hokuyo LIDAR is minus Infinity
@then("Range Message of TerraRanger One ROS node is minus infinity.")
def terranger_drone_altitude_minus_infinity(self):
    drone_terranger_altitude = laser_sub.getscanLaser_altitude()
    assert drone_terranger_altitude == -inf


################ When drone altitude between 0.2m and 14m ###############
@when('The drone is flying lower than 14 meters and higher than 0.2 meters above ground level')
def drone_flying_lower_thanb_14m_and_highen_than_0dot2m(self):
    low_altitude_threshold = gps_takeoff.low_altitude_threshold
    high_altitude_threshold = gps_takeoff.high_altitude_threshold
    drone_terranger_altitude =laser_sub.getscanLaser_altitude()
    assert low_altitude_threshold < drone_terranger_altitude < high_altitude_threshold

# Then the differece of the altitude received from Hokuyo LIDAR and the gps altitude is less than 0.15m
@then("The difference between the drone's altitude above ground level and Range Message of TerraRanger One ROS node is less then 0.30 meters.")
def difference_between_drone_altitude_and_terranger_altitude(self):
    altitude_difference =abs(gps_takeoff.get_gps_altitude() - gps_takeoff.get_initial_gps_altitude() - laser_sub.getscanLaser_altitude() )
#    altitude_difference = abs(gps_takeoff.get_current_z_pose() - laser_sub.getscanLaser_altitude())
    assert altitude_difference < 0.30


############# When drone altitude is higher than 14m ###############
@when('The drone is flying higher than 14 meters above ground level')
def drone_flying_higher_than_14m (self):
    high_altitude_threshold=gps_takeoff.high_altitude_threshold
    drone_terranger_altitude =laser_sub.getscanLaser_altitude()
    assert drone_terranger_altitude > high_altitude_threshold

# Then altitude received from Hokuyo LIDAR is plus Infinity
@then("Range Message of TerraRanger One ROS node is plus infinity.")
def terranger_drone_altitude_plus_infinity(self):
    drone_terranger_altitude = laser_sub.getscanLaser_altitude()
    assert drone_terranger_altitude == +inf





