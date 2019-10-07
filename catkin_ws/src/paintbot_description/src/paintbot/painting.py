#!/usr/bin/env python

from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from lib import constants
from trajectory_msgs.msg import JointTrajectoryPoint
import actionlib
import math
import rospy
import std_msgs
import trajectory_msgs

REST_POS = [0, 0, -math.pi / 2, math.pi, 0]
LOAD_POS_1 = [0, math.pi, -math.pi * 6 / 8, math.pi * 5 / 6, 0]
LOAD_POS_2 = [0, math.pi, -math.pi * 6 / 8, math.pi * 7 / 6, 0]
APPLY_HIGH_POS_1 = [0, math.pi / 2, -math.pi, math.pi, 0]
APPLY_HIGH_POS_2 = [0, math.pi / 2, -math.pi, 3.577925, 0]

arm_act_client = None
notify_pub = None

def move_arm(points):
    goal = FollowJointTrajectoryGoal()
    goal.trajectory.joint_names = ['arm_joint_1', 'arm_joint_2', 'arm_joint_3', 'arm_joint_4', 'arm_joint_5']
    goal.trajectory.points = points
    arm_act_client.send_goal(goal)
    arm_act_client.wait_for_result(rospy.Duration(20))

def handle_message(msg):
    if msg.data == constants.ACT_PAINT_LOAD:
        move_arm([
            JointTrajectoryPoint(positions=LOAD_POS_1, time_from_start=rospy.Duration(2)),
            JointTrajectoryPoint(positions=LOAD_POS_2, time_from_start=rospy.Duration(3)),
            JointTrajectoryPoint(positions=LOAD_POS_1, time_from_start=rospy.Duration(4)),
            JointTrajectoryPoint(positions=LOAD_POS_2, time_from_start=rospy.Duration(5)),
            JointTrajectoryPoint(positions=LOAD_POS_1, time_from_start=rospy.Duration(6)),
            JointTrajectoryPoint(positions=REST_POS, time_from_start=rospy.Duration(8))
        ])
        notify_pub.publish(constants.NOTIFY_ACT_COMPLETE)
    elif msg.data == constants.ACT_PAINT_APPLY:
        # TODO
        notify_pub.publish(constants.NOTIFY_ACT_COMPLETE)

def main():
    rospy.init_node('painting')

    global arm_act_client, notify_pub

    paint_sub = rospy.Subscriber(constants.TOPIC_PAINT, std_msgs.msg.String, handle_message)
    notify_pub = rospy.Publisher(constants.TOPIC_NOTIFY, std_msgs.msg.String, queue_size=10)

    arm_act_client = actionlib.SimpleActionClient(constants.TOPIC_ARM_SERVICE, FollowJointTrajectoryAction)
    arm_act_client.wait_for_server()

    # Move arm to rest position
    rest = JointTrajectoryPoint(positions=REST_POS, time_from_start=rospy.Duration(1))
    move_arm([rest])

    # TODO: Debug
    # move_arm([
    #     JointTrajectoryPoint(positions=APPLY_HIGH_POS_1, time_from_start=rospy.Duration(3)),
    #     JointTrajectoryPoint(positions=APPLY_HIGH_POS_2, time_from_start=rospy.Duration(4)),
    #     JointTrajectoryPoint(positions=APPLY_HIGH_POS_1, time_from_start=rospy.Duration(5)),
    #     JointTrajectoryPoint(positions=APPLY_HIGH_POS_2, time_from_start=rospy.Duration(6))
    # ])

    rospy.spin()
