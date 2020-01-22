#!/usr/bin/env python

from lib import constants, painting, util
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
import actionlib
import enum
import geometry_msgs
import math
import moveit_commander
import rospy
import std_msgs
import sys

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
    Task(constants.ACT_PAINT_APPLY, (-2, 0.5), 0)
]
t_i = 0
st = State.NAVIGATE

def navigate(task, mb_client):
    x = task.dest[0] + ((ACTION_DIST + WALL_THICKNESS) * math.cos(task.orientation))
    y = task.dest[1] + ((ACTION_DIST + WALL_THICKNESS) * math.sin(task.orientation))
    yaw = util.normalize_angle(task.orientation - math.pi)

    rospy.loginfo('Navigating to ({:.2f}, {:.2f}) @ {:.2f}'.format(x, y, yaw))

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation = geometry_msgs.msg.Quaternion(*quaternion_from_euler(0, 0, yaw))

    mb_client.send_goal(goal)
    wait = mb_client.wait_for_result()
    result = mb_client.get_result()

def act(task, mi_cmdr):
    if task.action == constants.ACT_PAINT_LOAD:
        painting.load_roller(mi_cmdr)
    elif task.action == constants.ACT_PAINT_APPLY:
        painting.apply(mi_cmdr)

def main():
    rospy.init_node('planning')
    rospy.loginfo('planning node starting...')

    rospy.loginfo('Setting up move_base client...')
    mb_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    mb_client.wait_for_server()

    rospy.loginfo('Setting up MoveIt commander...')
    moveit_commander.roscpp_initialize(sys.argv)
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    mi_cmdr = moveit_commander.MoveGroupCommander('arm')

    rospy.sleep(1) # TODO: Is there a better way to wait for everything to load?

    rospy.loginfo('planning node started')

    painting.move_arm_to_zero(mi_cmdr)

    i = 0
    while not rospy.is_shutdown():
        task = tasks[i]
        navigate(task, mb_client)
        rospy.sleep(1) # TODO: Debug
        act(task, mi_cmdr)
        i = (i + 1) % len(tasks)
