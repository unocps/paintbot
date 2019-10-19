#!/usr/bin/env python

import geometry_msgs.msg
import moveit_commander
import rospy
import sys

print('Setting up...')

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('mi_test', anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
move_group = moveit_commander.MoveGroupCommander('arm')

print('Moving arm...')

pose_goal = geometry_msgs.msg.Pose()
pose_goal.orientation.w = 1.0
pose_goal.position.x = 0.4
pose_goal.position.y = 0.1
pose_goal.position.z = 0.4
move_group.set_pose_target(pose_goal)

plan = move_group.go(wait=True)
move_group.stop()
move_group.clear_pose_targets()
