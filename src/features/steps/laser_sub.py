#!/usr/bin/env python

from re import I
from sensor_msgs.msg import LaserScan
import time
import rospy	
from math import inf


def scan_callback(scan_data):
    global scanLaser_altitude
#    scanLaser_altitude = scan_data.ranges[256]
    scanLaser_altitude =  min(scan_data.ranges)

def getscanLaser_altitude():
    
    try :
        rospy.init_node('scan_node',anonymous=True)
        rate = rospy.Rate(10)
        rospy.Subscriber('/spur/laser/scan',LaserScan,scan_callback,queue_size=10)
        rate.sleep()
        global scanLaser_altitude
        if scanLaser_altitude > 14:
            scanLaser_altitude= +inf
            return scanLaser_altitude
        elif scanLaser_altitude < 0.2:
            scanLaser_altitude = -inf 
            return scanLaser_altitude
        else : return scanLaser_altitude  

    except rospy.ROSInterruptException:
        pass

"""
if __name__ == '__main__':
    try:
        rospy.init_node('scan_node',anonymous=True)
        rospy.Subscriber('/spur/laser/scan',LaserScan,scan_callback,queue_size=10)
        print("publisher called")
        rospy.spin()      
    except rospy.ROSInterruptException:
        pass
"""


    
 	