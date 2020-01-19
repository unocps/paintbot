#!/usr/bin/env python

from lib import constants, util
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from paintbot_description.msg import PaintTarget
from tf.transformations import quaternion_from_euler
import actionlib
import enum
import geometry_msgs
import math
import rospy
import std_msgs

ACTION_DIST = 0.5
WALL_THICKNESS = 0.05

class Task:
    def __init__(self, action, dest, orientation):
        self.action = action
        self.dest = dest
        self.orientation = orientation

State = enum.Enum('State', 'NAVIGATE ACTION')

tasks = [
    Task(constants.ACT_PAINT_LOAD, (1, 1), -math.pi / 2),
    Task(constants.ACT_PAINT_APPLY, (-2, 1), 0)
]
t_i = 0
st = State.NAVIGATE
move_base_client = None
paint_pub = None

def navigate(x, y, yaw):
    goal_x = x + ((ACTION_DIST + WALL_THICKNESS) * math.cos(yaw))
    goal_y = y + ((ACTION_DIST + WALL_THICKNESS) * math.sin(yaw))
    goal_yaw = util.normalize_angle(yaw - math.pi)

    rospy.loginfo('Navigating to ({:.2f}, {:.2f}) @ {:.2f}'.format(goal_x, goal_y, goal_yaw))

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = goal_x
    goal.target_pose.pose.position.y = goal_y
    goal.target_pose.pose.orientation = geometry_msgs.msg.Quaternion(*quaternion_from_euler(0, 0, goal_yaw))

    move_base_client.send_goal(goal)
    wait = move_base_client.wait_for_result()
    result = move_base_client.get_result()

def handle_notification(msg):
    global t_i, st

    if msg.data == constants.NOTIFY_AT_DEST and st == State.NAVIGATE:
        task = tasks[t_i]
        st = State.ACTION
        msg = PaintTarget()
        msg.x = task.dest[0] + (WALL_THICKNESS * math.cos(task.orientation))
        msg.y = task.dest[1] + (WALL_THICKNESS * math.sin(task.orientation))
        msg.action = task.action

        rospy.sleep(1) # TODO: Debug

        paint_pub.publish(msg)
    elif msg.data == constants.NOTIFY_ACT_COMPLETE and st == State.ACTION:
        t_i = (t_i + 1) % len(tasks)
        task = tasks[t_i]
        rospy.loginfo('Beginning task {}'.format(task.action))
        st = State.NAVIGATE
        navigate(task.dest[0], task.dest[1], task.orientation)

def main():
    rospy.init_node('planning')
    rospy.loginfo('planning node starting...')

    global move_base_client, paint_pub

    rate = rospy.Rate(constants.ITERATION_RATE_HZ)

    rospy.loginfo('Connecting to topics...')
    notify_sub = rospy.Subscriber(constants.TOPIC_NOTIFY, std_msgs.msg.String, handle_notification)
    paint_pub = rospy.Publisher(constants.TOPIC_PAINT, PaintTarget, queue_size=10)

    rospy.loginfo('Setting for move_base client...')
    move_base_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    move_base_client.wait_for_server()

    rospy.sleep(1) # TODO: Is there a better way to wait for everything to load?

    rospy.loginfo('planning node started')

    # Send initial navigation command
    task = tasks[t_i]
    navigate(task.dest[0], task.dest[1], task.orientation)

    rospy.spin()
