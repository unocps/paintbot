#!/usr/bin/env python

from gazebo_msgs.msg import ModelStates
from lib import constants
import enum
import geometry_msgs
import math
import rospy
import std_msgs

class Task:
    def __init__(self, name, dest):
        self.name = name
        self.dest = dest

State = enum.Enum('State', 'NAVIGATE ACTION')

tasks = [
    Task('GET_PAINT', (2, 1)),
    Task('APPLY_PAINT', (-1, -1))
]
task_i = 0
st = State.NAVIGATE

def handle_notification(msg):
    global task_i

    if msg.data == constants.NOTIFY_AT_DEST and st == State.NAVIGATE:
        task_i = (task_i + 1) % len(tasks)
        # st = State.ACTION

def plan():
    rospy.init_node('planning')

    rate = rospy.Rate(constants.ITERATION_RATE_HZ)
    notify_sub = rospy.Subscriber('/paintbot/notify', std_msgs.msg.String, handle_notification)
    nav_pub = rospy.Publisher('/paintbot/nav', geometry_msgs.msg.Point, queue_size=10)

    while not rospy.is_shutdown():
        if st == State.NAVIGATE:
            dest = geometry_msgs.msg.Point()
            dest.x = tasks[task_i].dest[0]
            dest.y = tasks[task_i].dest[1]
            nav_pub.publish(dest)

        rate.sleep()
