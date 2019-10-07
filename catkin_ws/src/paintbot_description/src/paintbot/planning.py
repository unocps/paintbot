#!/usr/bin/env python

from gazebo_msgs.msg import ModelStates
from lib import constants
import enum
import geometry_msgs
import math
import rospy
import std_msgs

class Task:
    def __init__(self, action, dest):
        self.action = action
        self.dest = dest

State = enum.Enum('State', 'NAVIGATE ACTION')

tasks = [
    Task(constants.ACT_PAINT_LOAD, (2, 1)),
    Task(constants.ACT_PAINT_APPLY, (-1, -1))
]
t_i = 0
st = State.NAVIGATE
paint_pub = None
nav_pub = None

def handle_notification(msg):
    global t_i, st

    if msg.data == constants.NOTIFY_AT_DEST and st == State.NAVIGATE:
        st = State.ACTION
        paint_pub.publish(tasks[t_i].action)
    elif msg.data == constants.NOTIFY_ACT_COMPLETE and st == State.ACTION:
        t_i = (t_i + 1) % len(tasks)
        st = State.NAVIGATE
        dest = geometry_msgs.msg.Point()
        dest.x = tasks[t_i].dest[0]
        dest.y = tasks[t_i].dest[1]
        nav_pub.publish(dest)

def main():
    rospy.init_node('planning')

    global nav_pub, paint_pub

    rate = rospy.Rate(constants.ITERATION_RATE_HZ)
    notify_sub = rospy.Subscriber(constants.TOPIC_NOTIFY, std_msgs.msg.String, handle_notification)
    nav_pub = rospy.Publisher(constants.TOPIC_NAV, geometry_msgs.msg.Point, queue_size=10)
    paint_pub = rospy.Publisher(constants.TOPIC_PAINT, std_msgs.msg.String, queue_size=10)

    rospy.sleep(1) # TODO: Is there a better way to wait for everything to load?

    # Send initial navigation command
    dest = geometry_msgs.msg.Point()
    dest.x = tasks[t_i].dest[0]
    dest.y = tasks[t_i].dest[1]
    nav_pub.publish(dest)

    rospy.spin()
