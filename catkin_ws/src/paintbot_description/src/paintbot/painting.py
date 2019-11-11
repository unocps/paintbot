#!/usr/bin/env python

from gazebo_msgs.msg import ModelStates
from lib import constants, util
from paintbot_description.msg import PaintTarget
from tf.transformations import euler_from_quaternion
import math
import moveit_commander
import rospy
import std_msgs
import sys

_ARM_OFFSET = (0.166990, 0, 0.142000)
_NUM_PASSES = 3
_PAINT_Z = (0.4, 0.25)

_arm_origin = None
_move_group = None
_notify_pub = None

def move_arm_to_zero():
    rospy.loginfo('Moving arm to zero position')
    _move_group.set_joint_value_target(_move_group.get_named_target_values('zero'))
    _move_group.go(wait=True)
    _move_group.stop()
    _move_group.clear_pose_targets()
    rospy.loginfo('Arm at zero position')

# TODO: Look into move_group.compute_cartesian_path()
def paint(target):
    rospy.loginfo('Applying paint...')

    arm_orient = math.atan2(target[1] - _arm_origin[1], target[0] - _arm_origin[0])

    for i in range(_NUM_PASSES * 2 + 1):
        _move_group.set_pose_target([
            _arm_origin[0] + (target[0] * math.cos(arm_orient)),
            _arm_origin[1] + (target[0] * math.sin(arm_orient)),
            _PAINT_Z[i % 2],
            0,
            -math.pi / 2,
            math.pi + arm_orient])
        _move_group.go(wait=True)
        _move_group.stop()
        _move_group.clear_pose_targets()

    rospy.loginfo('Finished applying paint')

def update_robot_state(msg):
    if constants.ROBOT_NAME in msg.name:
        i = msg.name.index(constants.ROBOT_NAME)
        pose = msg.pose[i].position
        o = msg.pose[i].orientation
        orient = util.normalize_angle(euler_from_quaternion([o.x, o.y, o.z, o.w])[2])

        global _arm_origin
        _arm_origin = (pose.x + (_ARM_OFFSET[0] * math.cos(orient)), pose.y + (_ARM_OFFSET[0] * math.sin(orient)), _ARM_OFFSET[2])

def handle_message(msg):
    if msg.action == constants.ACT_PAINT_LOAD:
        # TODO
        _notify_pub.publish(constants.NOTIFY_ACT_COMPLETE)
    elif msg.action == constants.ACT_PAINT_APPLY:
        paint((msg.x, msg.y))
        _notify_pub.publish(constants.NOTIFY_ACT_COMPLETE)

def main():
    global _move_group, _notify_pub

    rospy.loginfo('painting node starting...')

    rospy.init_node('painting')

    paint_sub = rospy.Subscriber(constants.TOPIC_PAINT, PaintTarget, handle_message)
    model_states_sub = rospy.Subscriber(constants.TOPIC_MODEL_STATES, ModelStates, update_robot_state)
    _notify_pub = rospy.Publisher(constants.TOPIC_NOTIFY, std_msgs.msg.String, queue_size=10)

    moveit_commander.roscpp_initialize(sys.argv)
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    _move_group = moveit_commander.MoveGroupCommander('arm')

    move_arm_to_zero()

    rospy.loginfo('painting node started')

    rospy.spin()
