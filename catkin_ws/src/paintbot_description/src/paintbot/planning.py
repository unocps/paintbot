#!/usr/bin/env python

from gazebo_msgs.msg import ModelStates
from lib import constants, util
from paintbot_description.msg import PaintTarget
from tf.transformations import quaternion_from_euler
import enum
import geometry_msgs
import math
import rospy
import std_msgs

ACTION_DIST = 0.5
WALL_THICKNESS = 0.05

class Task:
    def __init__(self, action, dest, orient):
        self.action = action
        self.dest = dest
        self.orient = orient

State = enum.Enum('State', 'NAVIGATE ACTION')

tasks = [
    Task(constants.ACT_PAINT_LOAD, (1, 1), -math.pi / 2),
    Task(constants.ACT_PAINT_APPLY, (-2, 1), 0)
]
t_i = 0
st = State.NAVIGATE
paint_pub = None
nav_pub = None

def handle_notification(msg):
    global t_i, st

    if msg.data == constants.NOTIFY_AT_DEST and st == State.NAVIGATE:
        task = tasks[t_i]
        st = State.ACTION
        msg = PaintTarget()
        msg.x = task.dest[0] + (WALL_THICKNESS * math.cos(task.orient))
        msg.y = task.dest[1] + (WALL_THICKNESS * math.sin(task.orient))
        msg.action = task.action

        rospy.sleep(1) # TODO: Debug

        paint_pub.publish(msg)
    elif msg.data == constants.NOTIFY_ACT_COMPLETE and st == State.ACTION:
        t_i = (t_i + 1) % len(tasks)
        task = tasks[t_i]
        rospy.loginfo('Beginning task {}'.format(task.action))
        st = State.NAVIGATE
        dest = geometry_msgs.msg.Pose()
        dest.position.x = task.dest[0] + ((ACTION_DIST + WALL_THICKNESS) * math.cos(task.orient))
        dest.position.y = task.dest[1] + ((ACTION_DIST + WALL_THICKNESS) * math.sin(task.orient))
        dest.orientation = geometry_msgs.msg.Quaternion(*quaternion_from_euler(0, 0, util.normalize_angle(task.orient - math.pi)))
        nav_pub.publish(dest)

def main():
    rospy.init_node('planning')
    rospy.loginfo('planning node starting...')

    global nav_pub, paint_pub

    rate = rospy.Rate(constants.ITERATION_RATE_HZ)
    notify_sub = rospy.Subscriber(constants.TOPIC_NOTIFY, std_msgs.msg.String, handle_notification)
    nav_pub = rospy.Publisher(constants.TOPIC_NAV, geometry_msgs.msg.Pose, queue_size=10)
    paint_pub = rospy.Publisher(constants.TOPIC_PAINT, PaintTarget, queue_size=10)

    rospy.sleep(1) # TODO: Is there a better way to wait for everything to load?

    # Send initial navigation command
    task = tasks[t_i]
    dest = geometry_msgs.msg.Pose()
    dest.position.x = task.dest[0] + ((ACTION_DIST + WALL_THICKNESS) * math.cos(task.orient))
    dest.position.y = task.dest[1] + ((ACTION_DIST + WALL_THICKNESS) * math.sin(task.orient))
    dest.orientation = geometry_msgs.msg.Quaternion(*quaternion_from_euler(0, 0, util.normalize_angle(task.orient - math.pi)))
    nav_pub.publish(dest)

    rospy.loginfo('planning node started')

    rospy.spin()
