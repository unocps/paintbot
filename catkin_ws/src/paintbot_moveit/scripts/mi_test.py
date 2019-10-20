#!/usr/bin/env python

from tf.transformations import quaternion_from_euler
import geometry_msgs.msg
import math
import moveit_commander
import rospy
import sys

def move_arm_to_zero(move_group):
    print('Moving arm to zero position')
    move_group.set_joint_value_target(move_group.get_named_target_values('zero'))
    plan = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

def move_arm(goal):
    print('Moving arm to {}'.format(goal))

    ARM_OFFSET = (0.166990, 0, 0.142000)
    # arm_origin = robot_pose + ARM_OFFSET (and take facing into account)

    arm_facing_goal = math.atan2(goal[1] - ARM_OFFSET[1], goal[0] - ARM_OFFSET[0])
    print('arm_facing_goal: {}'.format(arm_facing_goal))

    q = quaternion_from_euler(0, -math.pi / 2, math.pi + arm_facing_goal)
    pose_goal = geometry_msgs.msg.Pose()
    pose_goal.orientation.x = q[0]
    pose_goal.orientation.y = q[1]
    pose_goal.orientation.z = q[2]
    pose_goal.orientation.w = q[3]
    pose_goal.position.x = goal[0]
    pose_goal.position.y = goal[1]
    pose_goal.position.z = goal[2]
    move_group.set_pose_target(pose_goal)

    plan = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

print('Setting up...')

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('mi_test', anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
move_group = moveit_commander.MoveGroupCommander('arm')

# print('End effector link: {}'.format(move_group.get_end_effector_link()))

move_arm_to_zero(move_group)
move_arm((0.2, 0.2, 0.4))
move_arm((0.5, 0.0, 0.2))

# print(move_group.get_current_pose(move_group.get_end_effector_link()))
# print(move_group.get_current_rpy(move_group.get_end_effector_link()))
