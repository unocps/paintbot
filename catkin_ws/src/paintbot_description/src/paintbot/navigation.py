#!/usr/bin/env python

from gazebo_msgs.msg import ModelStates
from lib import constants, util
from tf.transformations import euler_from_quaternion
import geometry_msgs
import math
import rospy
import std_msgs

# TODO: These tolerances are too high and should be fixed, possibly by better wheel controller
DIST_EPSILON = 0.1
ORIENT_EPSILON = 0.05
MAX_SPEED = 0.2

pose = None
dest = None

def update_state(msg):
    if constants.ROBOT_NAME in msg.name:
        global pose
        i = msg.name.index(constants.ROBOT_NAME)
        o = msg.pose[i].orientation
        pose = (msg.pose[i].position.x, msg.pose[i].position.y, util.normalize_angle(euler_from_quaternion((o.x, o.y, o.z, o.w))[2]))

def update_dest(msg):
    global dest
    dest = (msg.position.x, msg.position.y, euler_from_quaternion((msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w))[2])
    rospy.loginfo('Destination updated: ({}, {}) @ {}'.format(dest[0], dest[1], dest[2]))

def at_dest():
    dist = math.sqrt(((pose[0] - dest[0]) ** 2) + ((pose[1] - dest[1]) ** 2))
    return dist <= DIST_EPSILON

def facing_dest():
    target = math.atan2(dest[1] - pose[1], dest[0] - pose[0]) if not at_dest() else dest[2]
    theta = util.normalize_angle(target - pose[2])
    return abs(theta) <= ORIENT_EPSILON

def adjust_orientation(pub):
    target = math.atan2(dest[1] - pose[1], dest[0] - pose[0]) if not at_dest() else dest[2]
    theta = util.normalize_angle(target - pose[2])
    twist = geometry_msgs.msg.Twist()
    twist.angular.z = -1 if theta < 0 else 1
    pub.publish(twist)

def move(pub):
    twist = geometry_msgs.msg.Twist()
    twist.linear.x = MAX_SPEED
    pub.publish(twist)

def main():
    rospy.init_node('navigation')

    rospy.loginfo('navigation node starting...')

    rate = rospy.Rate(constants.ITERATION_RATE_HZ)
    model_states_sub = rospy.Subscriber(constants.TOPIC_MODEL_STATES, ModelStates, update_state)
    nav_sub = rospy.Subscriber(constants.TOPIC_NAV, geometry_msgs.msg.Pose, update_dest)
    dd_pub = rospy.Publisher(constants.TOPIC_CMD_VEL, geometry_msgs.msg.Twist, queue_size=10)
    notify_pub = rospy.Publisher(constants.TOPIC_NOTIFY, std_msgs.msg.String, queue_size=10)

    global dest

    rospy.loginfo('navigation node started')

    while not rospy.is_shutdown():
        if pose and dest:
            if not facing_dest():
                adjust_orientation(dd_pub)
            elif not at_dest():
                move(dd_pub)
            else:
                rospy.loginfo('Destination reached: ({}, {}) @ {}'.format(pose[0], pose[1], pose[2]))
                notify_pub.publish(constants.NOTIFY_AT_DEST)
                dest = None
        else:
            # Stop
            dd_pub.publish(geometry_msgs.msg.Twist())

        rate.sleep()
