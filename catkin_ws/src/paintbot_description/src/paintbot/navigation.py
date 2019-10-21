#!/usr/bin/env python

from gazebo_msgs.msg import ModelStates
from lib import constants
from tf.transformations import euler_from_quaternion
import geometry_msgs
import math
import rospy
import std_msgs

DIST_EPSILON = 0.75
ORIENT_EPSILON = 0.1
MAX_SPEED = 0.2

pose = None
orient = None
dest = None

def normalize_angle(theta):
    if theta < -math.pi:
        theta += 2 * math.pi
    if theta > math.pi:
        theta -= 2 * math.pi
    return theta

def update_state(msg):
    if 'paintbot' in msg.name:
        global pose, orient
        i = msg.name.index('paintbot')
        pose = msg.pose[i].position
        o = msg.pose[i].orientation
        orient = normalize_angle(euler_from_quaternion([o.x, o.y, o.z, o.w])[2])

def update_dest(msg):
    global dest
    dest = msg

def at_dest():
    if pose:
        dist = math.sqrt(((pose.x - dest.x) ** 2) + ((pose.y - dest.y) ** 2))
        return dist < DIST_EPSILON
    return false

def adjust_orientation(pub):
    theta = normalize_angle(math.atan2(dest.y - pose.y, dest.x - pose.x) - orient)
    while abs(theta) > ORIENT_EPSILON:
        print('adjust_orientation: {}'.format(theta))
        twist = geometry_msgs.msg.Twist()
        twist.angular.z = -1 if theta < 0 else 1
        pub.publish(twist)
        theta = normalize_angle(math.atan2(dest.y - pose.y, dest.x - pose.x) - orient)

def move(pub):
    twist = geometry_msgs.msg.Twist()
    twist.linear.x = MAX_SPEED
    pub.publish(twist)

def main():
    rospy.init_node('navigation')

    rate = rospy.Rate(constants.ITERATION_RATE_HZ)
    model_states_sub = rospy.Subscriber(constants.TOPIC_MODEL_STATES, ModelStates, update_state)
    nav_sub = rospy.Subscriber(constants.TOPIC_NAV, geometry_msgs.msg.Point, update_dest)
    dd_pub = rospy.Publisher(constants.TOPIC_DIFF_DRIVE, geometry_msgs.msg.Twist, queue_size=10)
    notify_pub = rospy.Publisher(constants.TOPIC_NOTIFY, std_msgs.msg.String, queue_size=10)

    global pose, orient, dest

    while not rospy.is_shutdown():
        if pose and orient and dest:
            if at_dest():
                notify_pub.publish(constants.NOTIFY_AT_DEST)
                dest = None
            else:
                adjust_orientation(dd_pub)
                move(dd_pub)
        else:
            # Stop
            dd_pub.publish(geometry_msgs.msg.Twist())

        rate.sleep()
