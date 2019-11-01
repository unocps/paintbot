#!/usr/bin/env python

from gazebo_msgs.msg import ModelStates
from tf.transformations import euler_from_quaternion
import math
import moveit_commander
import rospy
import sys

_ARM_OFFSET = (0.166990, 0, 0.142000)
_NUM_PASSES = 3
_PAINT_Z = (0.4, 0.25)

_arm_origin = _ARM_OFFSET

# TODO: Move to lib
def normalize_angle(theta):
    if theta < -math.pi:
        theta += 2 * math.pi
    if theta > math.pi:
        theta -= 2 * math.pi
    return theta

# TODO: Proper ROS logging

def update_state(msg):
    if 'paintbot' in msg.name:
        i = msg.name.index('paintbot')
        pose = msg.pose[i].position
        o = msg.pose[i].orientation
        orient = normalize_angle(euler_from_quaternion([o.x, o.y, o.z, o.w])[2])

        global _arm_origin
        _arm_origin = (pose[0] + (_ARM_OFFSET[0] * math.cos(orient)), pose[1] + (_ARM_OFFSET[0] * math.sin(orient)), _ARM_OFFSET[2])

def move_arm_to_zero(move_group):
    print('Moving arm to zero position')
    move_group.set_joint_value_target(move_group.get_named_target_values('zero'))
    plan = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

def move_arm(move_group, goal):
    print('Moving arm to {}'.format(goal))

    arm_facing_goal = math.atan2(goal[1] - _arm_origin[1], goal[0] - _arm_origin[0])

    move_group.set_pose_target([goal[0], goal[1], goal[2], 0, -math.pi / 2, math.pi + arm_facing_goal])
    plan = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

# TODO: Look into move_group.compute_cartesian_path()
def paint(move_group, target):
    print('Applying paint...')

    arm_orient = math.atan2(target[1] - _arm_origin[1], target[0] - _arm_origin[0])

    for i in range(_NUM_PASSES * 2 + 1):
        move_group.set_pose_target([
            _arm_origin[0] + (target[0] * math.cos(arm_orient)),
            _arm_origin[1] + (target[0] * math.sin(arm_orient)),
            _PAINT_Z[i % 2],
            0,
            -math.pi / 2,
            math.pi + arm_orient])
        plan = move_group.go(wait=True)
        move_group.stop()
        move_group.clear_pose_targets()

    print('Finished applying paint.')

print('Setting up...')

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('mi_test', anonymous=True)

model_states_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, update_state)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
move_group = moveit_commander.MoveGroupCommander('arm')

move_arm_to_zero(move_group)
# move_arm(move_group, (0.2, 0.2, 0.4))
paint(move_group, (0.2, 0.2))

# print(move_group.get_current_pose(move_group.get_end_effector_link()))
# print(move_group.get_current_rpy(move_group.get_end_effector_link()))
