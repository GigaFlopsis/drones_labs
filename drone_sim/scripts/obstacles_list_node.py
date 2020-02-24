#!/usr/bin/env python
# coding: utf-8

"""
The node for integration diagnostics from subsystems (mavros/pixhawk)
"""

import rospy
from rospy import Header
from geometry_msgs.msg import PoseArray, Pose, Point
import copy


scale_collum = [0.2, 3.0]

obstacles_array = PoseArray()
obstacles_array.header.frame_id = 'map'

array = ([2.0,0.0],
         [6.5,-1.9],
         [5.0,-0.5],
         [3.5,0.5],
         [2.8,2.0],
         [7.5,-0.8],
         [6.5,0.8],
         [5.0,1.8],
         [7.0,2.9],
         [9.2,1.3],
         [9.5,-0.7],
         [3.5,-3.0])

def update_collum(x,y):
    global marker_collms
    collum = Pose()
    collum.position.x = x
    collum.position.y = y
    collum.position.z = 1.5
    collum.orientation.w = 1.
    obstacles_array.poses.append(collum)


for i in array:
    update_collum(i[0],i[1])



### main
if __name__ == '__main__':

    rospy.init_node('obstacles_list_node', anonymous=True)
    rate = rospy.Rate(10)       # set rate

    # publisher
    obst_pub = rospy.Publisher("obstacles", PoseArray,queue_size=10)

    # loop
    try:
        while not rospy.is_shutdown():
            obstacles_array.header.stamp = rospy.Time.now()

            obst_pub.publish(obstacles_array)

            rate.sleep()
    except:
         print("exit")
         raise
