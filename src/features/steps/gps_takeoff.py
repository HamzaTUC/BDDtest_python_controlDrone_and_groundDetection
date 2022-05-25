#!/usr/bin/env python3

#import library ros 
#import mavros_msgs
import rospy 
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from std_msgs.msg import String
from std_msgs.msg import Float32
from mavros_msgs.msg import State
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TwistStamped
from mavros_msgs.srv import SetMode
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import CommandTOL
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import NavSatFix



bool_takeoff= True
bool_land=True
alt_set = 1
goal_pose = PoseStamped() # renaming PoseStamped 
current_state = State() # renaming state 
gps_read = False # When starting gps read will be sent to false initially
goal_pose = PoseStamped() 

low_altitude_threshold = 0.2
high_altitude_threshold = 14
max_altitude = 20
count=0

def scan_callback(scan_data):
    global bool_land
    global bool_takeoff

    if (low_altitude_threshold < scan_data.ranges[256] and scan_data.ranges[256] < max_altitude): 
        print("----------------Distance sensor Value:", scan_data.ranges[256])
        print("----------------min Distance sensor Value:", min(scan_data.ranges))
        print("----------------Distance GPS Value:", gps.altitude)
        print("----------------Initial gps altitude  GPS Value:", get_initial_gps_altitude())
        print("----------------difference with gsp using min():", gps.altitude -get_initial_gps_altitude() - min(scan_data.ranges) )
        print("----------------difference with gsp using index 256 :", gps.altitude -get_initial_gps_altitude() - scan_data.ranges[256] )
    #    print("----------------difference with z pose is :", get_current_z_pose() - scan_data.ranges[256] )
        print(f"OK ---- Drone is between {low_altitude_threshold} m and {max_altitude} m ") 
        
    elif (scan_data.ranges[256]< low_altitude_threshold): 
        print(" Minus Infinity, Real is: ",scan_data.ranges[256])  
        print("----------------min Distance sensor Value:", min(scan_data.ranges))
        print("--------------- Initial gps altitude : ",get_initial_gps_altitude()) 
        print("----------------Distance GPS Value:", gps.altitude)
    #    print("----------------Distance GPS Value:", get_current_z_pose())
        print("----------------difference with gsp using min():", gps.altitude -get_initial_gps_altitude() - min(scan_data.ranges) )
        print("----------------difference with gsp using index 256 :", gps.altitude -get_initial_gps_altitude() - scan_data.ranges[256] )
    #    print("----------------difference with z pose is :", get_current_z_pose() - scan_data.ranges[256] )
        print(f"{low_altitude_threshold} m minimum distance threshold reached, send takeoff command")
        if bool_takeoff:
            cmd_offboard_mode()
            cmd_arm()
            cmd_takeoff()
            bool_takeoff=False  
            bool_land=True  

    else:  
        print("Plus Infinity, real is: ", scan_data.ranges[256])   
        print("----------------min Distance sensor Value:", min(scan_data.ranges))
        print("----------------Distance GPS Value:", gps.altitude)
        print("----------------Initial gps altitude : ",get_initial_gps_altitude())
        print("----------------difference with gsp using min():", gps.altitude -get_initial_gps_altitude() - min(scan_data.ranges) )
        print("----------------difference with gsp using index 256 :", gps.altitude -get_initial_gps_altitude() - scan_data.ranges[256] )
    #    print("----------------difference with z pose is :", get_current_z_pose() - scan_data.ranges[256] )
        print(f"{max_altitude} m max distance threshold reached, send land command") 
        if bool_land == 1:
            cmd_land()
            bool_land=False    
            bool_takeoff=True


def state_callback(data):
    cur_state = data
    # Gets state from /mavros/state
    

def pose_sub_callback(pose_sub_data):
    global current_pose
    current_pose = pose_sub_data
    # Callback function to get current position for FCU   


def get_current_z_pose():
    return current_pose.pose.position.z   


"""
def get_current_z_pose():
    try:
        rospy.init_node('scan_node',anonymous=True)
        rate = rospy.Rate(10)
        rospy.Subscriber('/mavros/local_position/pose', PoseStamped, pose_sub_callback) 
        rate.sleep()    
        global current_pose
        return current_pose.pose.position.z
    except rospy.ROSInterruptException:
        print("ROSInterrupt Exception ")
"""
    

def gps_callback(data):
    global gps 
    gps = data
    gps_read = True

def get_gsp_altitude():
    return gps.altitude

def get_initial_gps_altitude():
    global initial_gps_altitude
    global count
    if count == 0: 
        initial_gps_altitude = gps.altitude
        count=1
    if initial_gps_altitude > 537:     
        initial_gps_altitude = 535.34
        return initial_gps_altitude    
    else:          
        return initial_gps_altitude
    
## Takeoff part ###
def cmd_takeoff():

    takeoff = rospy.ServiceProxy('/mavros/cmd/takeoff', CommandTOL)
    # Take off
    current_altitude = gps.altitude 
    print('\n Takeoff')
    rospy.wait_for_service('/mavros/cmd/takeoff')
    try:		
        min_pitch = 0
        yaw = 0
        latitude = gps.latitude
        longitude = gps.longitude
        altitude = alt_set
        mode_guided = takeoff(min_pitch, yaw, latitude, longitude, altitude)
        if mode_guided:
            rospy.loginfo("Took-off")
        else:
            rospy.loginfo("Failed taking-off")
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed")
    
    # Keep sending take-off messages until received by FCU
    while not mode_guided:
        rate.sleep()
        mode_guided = takeoff(min_pitch, yaw, latitude, longitude, altitude)
        if mode_guided:
            rospy.loginfo("Took-off")
        else:
            rospy.loginfo("Failed taking-off")

    while gps.altitude< current_altitude+altitude-0.1:
        rate.sleep()
        differ = gps.altitude - current_altitude
        rospy.loginfo("Waiting to take off, current height %s", differ)

    # Position
    print(current_pose.pose.position.x)
    goal_pose.header.frame_id = "8"
    goal_pose.header.seq = 1
    goal_pose.pose.position.x = 0
    goal_pose.pose.position.y = 0 
    goal_pose.pose.position.z = 20
    local_position_pub.publish(goal_pose)
    rospy.loginfo(goal_pose)

def cmd_offboard_mode():
    last_request = rospy.get_rostime()
    # set offboard
    change_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
    rospy.wait_for_service('/mavros/set_mode')
    try:
        base_mode = 0
        custom_mode = "GUIDED"
        mode_guided = change_mode(base_mode, custom_mode)
        print(mode_guided)
        if mode_guided:
            rospy.loginfo("GUIDED mode set")
        else:
            rospy.loginfo("Failed SetMode")
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed")
    last_request = rospy.get_rostime() 
    
    while not mode_guided:
        rate.sleep()
        mode_guided = change_mode(base_mode, custom_mode)
        if mode_guided:
            rospy.loginfo("setmode send ok value")
        else:
            rospy.loginfo("Failed SetMode")
    
def cmd_arm():
    # Arm drone
    arm = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        armed = arm(True)
        if armed:
            rospy.loginfo("Armed")
        else:
            rospy.loginfo("Failed Arming")
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed")
    last_request = rospy.get_rostime() 
    
    while not armed:
        rate.sleep()
        armed = arm(True)
        if armed:
            rospy.loginfo("Armed")
        else:
            rospy.loginfo("Failed Arming")


def cmd_land():
    # Landing
    print ("\nLanding")
    rospy.wait_for_service('/mavros/cmd/land')
    try:
        landing_cl = rospy.ServiceProxy('/mavros/cmd/land', CommandTOL)
        response = landing_cl(altitude=2, latitude=0, longitude=0, min_pitch=0, yaw=0)
        rospy.loginfo(response)
    except rospy.ServiceException as e:
        print("Landing failed: %s" %e)
        rospy.signal_shutdown(True)
        rospy.loginfo("\n Pilot Takeover!")

def get_gps_altitude():
    rospy.init_node('scan_node',anonymous=True)
    rate = rospy.Rate(10)
    rospy.Subscriber("/mavros/global_position/global", NavSatFix, gps_callback)
    rate.sleep()
    return gps.altitude   

if __name__== "__main__":

    try:
        rospy.init_node('scan_node',anonymous=True)
        rate = rospy.Rate(10)
        rospy.Subscriber("/mavros/global_position/global", NavSatFix, gps_callback)
        local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 10) 
        local_position_subscribe = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, pose_sub_callback) # Getting current position and sets current_pose to subscribed value
        rospy.Subscriber('/spur/laser/scan',LaserScan,scan_callback,queue_size=10)
        rospy.Subscriber("/mavros/state", State, state_callback) 
#        local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 10) 
#        setpoint_velocity_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel',TwistStamped, queue_size = 10)
        while not gps_read:
            rate.sleep()    
        print("laser scan publisher called")
        rospy.spin()      
        

    except rospy.ROSInterruptException:
        print("ROSInterrupt Exception ")






    
    
   



   
    
    
  


