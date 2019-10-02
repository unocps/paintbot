#!/usr/bin/env python

from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from lib import constants
from trajectory_msgs.msg import JointTrajectoryPoint
import actionlib
import rospy
import std_msgs
import trajectory_msgs

def handle_message(msg):
    pass

def main():
    rospy.init_node('painting')

    rospy.sleep(1)

    paint_sub = rospy.Subscriber(constants.TOPIC_PAINT, std_msgs.msg.String, handle_message)
    arm_action_client = actionlib.SimpleActionClient(constants.TOPIC_ARM_SERVICE, FollowJointTrajectoryAction)
    arm_action_client.wait_for_server()

    goal = FollowJointTrajectoryGoal()
    goal.trajectory.joint_names = ['arm_joint_1', 'arm_joint_2', 'arm_joint_3', 'arm_joint_4', 'arm_joint_5']
    point = JointTrajectoryPoint()
    point.positions = [.5, .5, .5, .5, .5]
    point.time_from_start = rospy.Duration(5)
    goal.trajectory.points = [point]

    arm_action_client.send_goal(goal)
    arm_action_client.wait_for_result(rospy.Duration(10))

    rospy.sleep(5)

    goal = FollowJointTrajectoryGoal()
    goal.trajectory.joint_names = ['arm_joint_1', 'arm_joint_2', 'arm_joint_3', 'arm_joint_4', 'arm_joint_5']
    point = JointTrajectoryPoint()
    point.positions = [3, 3, 3, 3, 3]
    point.time_from_start = rospy.Duration(5)
    goal.trajectory.points = [point]

    arm_action_client.send_goal(goal)
    arm_action_client.wait_for_result(rospy.Duration(10))
