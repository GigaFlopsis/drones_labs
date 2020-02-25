#!/usr/bin/env python
# coding: utf-8

"""
The node for integration diagnostics from subsystems (mavros/pixhawk)
"""

import rospy
from rospy import Header
from geometry_msgs.msg import PoseArray, Pose, Point
from visualization_msgs.msg import Marker, MarkerArray
import copy


scale_collum = [0.4, 3.0]

obstacles_array = PoseArray()
marker_array = MarkerArray()
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

def setup_market(x,y,z,id):
    """
    Настройка маркера для отображения в rviz
    :type point: Point
    :param point:
    :return:
    """
    marker = Marker()
    marker.header.frame_id = "map"
    marker.header.stamp = rospy.get_rostime()
    marker.ns = "collum"
    marker.id = id
    marker.action = 0
    marker.pose.orientation.x = 0
    marker.pose.orientation.y = 0
    marker.pose.orientation.z = 0
    marker.pose.orientation.w = 1.0

    marker.scale.x = scale_collum[0]
    marker.scale.y = scale_collum[0]
    marker.scale.z = scale_collum[1]
    marker.type = Marker.CYLINDER
    marker.color.r = 1.
    marker.color.g = 0.
    marker.color.b = 0.
    marker.color.a = 1.
    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = z

    return marker

def update_collum(x,y, id):
    global marker_collms, marker_array
    collum = Pose()
    collum.position.x = x
    collum.position.y = y
    collum.position.z = 1.5
    collum.orientation.w = 1.
    obstacles_array.poses.append(collum)
    marker_array.markers.append(setup_market(x,y,1.5,id))


### main
if __name__ == '__main__':

    rospy.init_node('obstacles_list_node', anonymous=True)
    rate = rospy.Rate(10)       # set rate

    # publisher
    obst_pub = rospy.Publisher("obstacles", PoseArray,queue_size=10)
    marker_pub = rospy.Publisher("obstacles/markers", MarkerArray,queue_size=10)
    k = 0
    for i in array:
        update_collum(i[0], i[1],k)
        k = k+1

    # loop
    try:
        while not rospy.is_shutdown():
            obstacles_array.header.stamp = rospy.Time.now()
            marker_pub.publish(marker_array)
            obst_pub.publish(obstacles_array)

            rate.sleep()
    except:
         print("exit")
         raise
