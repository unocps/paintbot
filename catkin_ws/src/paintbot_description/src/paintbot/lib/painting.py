#!/usr/bin/env python

from . import constants, util
import math
import moveit_commander
import rospy

_ARM_OFFSET = (0.166990, 0, 0.142000)
_NUM_PASSES = 3
_PAINT_Z = (0.4, 0.25)
_LOAD_X = (0.375, 0.475)

def move_arm_to_zero(mi_cmdr, wait=False):
    rospy.loginfo('Moving arm to zero position')
    mi_cmdr.set_joint_value_target(mi_cmdr.get_named_target_values('zero'))
    mi_cmdr.go(wait=wait)
    mi_cmdr.stop()
    mi_cmdr.clear_pose_targets()
    rospy.loginfo('Arm at zero position')

# TODO: Look into move_group.compute_cartesian_path()
def apply(mi_cmdr):
    rospy.loginfo('Applying paint...')

    for i in range(_NUM_PASSES * 2 + 1):
        mi_cmdr.set_pose_target([0.4, 0, _PAINT_Z[i % 2], 0, -math.pi / 2, math.pi])
        mi_cmdr.go(wait=True)
        mi_cmdr.stop()
        mi_cmdr.clear_pose_targets()

    move_arm_to_zero(mi_cmdr)

    rospy.loginfo('Finished applying paint')

def load_roller(mi_cmdr):
    rospy.loginfo('Loading paint roller...')

    for i in range(_NUM_PASSES * 2 + 1):
        mi_cmdr.set_pose_target([_LOAD_X[i % 2], 0, 0.05, -math.pi, 0, -math.pi])
        mi_cmdr.go(wait=True)
        mi_cmdr.stop()
        mi_cmdr.clear_pose_targets()

    move_arm_to_zero(mi_cmdr)

    rospy.loginfo('Finished loading paint roller')
