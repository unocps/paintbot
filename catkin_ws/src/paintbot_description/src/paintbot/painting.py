#!/usr/bin/env python

from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from lib import constants
from trajectory_msgs.msg import JointTrajectoryPoint
import actionlib
import math
import rospy
import std_msgs
import trajectory_msgs

# TODO: Positions may need to be turned around so that arm_joint_1 rests at 0
REST_POS = [math.pi, 0, -1, 0, 0]
LOAD_POS_1 = [math.pi, 0, -math.pi * (7 / 6), .1, 0]
LOAD_POS_2 = [math.pi, 0, -math.pi * (7 / 6), .75, 0]

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
        points = [
            JointTrajectoryPoint(positions=LOAD_POS_1, time_from_start=rospy.Duration(2)),
            JointTrajectoryPoint(positions=LOAD_POS_2, time_from_start=rospy.Duration(3)),
            JointTrajectoryPoint(positions=LOAD_POS_1, time_from_start=rospy.Duration(4)),
            JointTrajectoryPoint(positions=LOAD_POS_2, time_from_start=rospy.Duration(5)),
            JointTrajectoryPoint(positions=LOAD_POS_1, time_from_start=rospy.Duration(6)),
            JointTrajectoryPoint(positions=REST_POS, time_from_start=rospy.Duration(8)),
        ]
        move_arm(points)
        notify_pub.publish(constants.NOTIFY_ACT_COMPLETE)
    elif msg.data == constants.ACT_PAINT_APPLY:
        # TODO
        notify_pub.publish(constants.NOTIFY_ACT_COMPLETE)

def main():
    rospy.init_node('painting')

    global arm_act_client, notify_pub

    # TODO: Is this necessary to give the controller time to start?
    rospy.sleep(0.5)

    paint_sub = rospy.Subscriber(constants.TOPIC_PAINT, std_msgs.msg.String, handle_message)
    notify_pub = rospy.Publisher(constants.TOPIC_NOTIFY, std_msgs.msg.String, queue_size=10)

    arm_act_client = actionlib.SimpleActionClient(constants.TOPIC_ARM_SERVICE, FollowJointTrajectoryAction)
    arm_act_client.wait_for_server()

    # Move arm to rest position
    rest = JointTrajectoryPoint(positions=REST_POS, time_from_start=rospy.Duration(1))
    move_arm([rest])

    rospy.spin()
