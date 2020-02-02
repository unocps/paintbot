#!/usr/bin/env python

from skiros2_common.core.primitive import PrimitiveBase
from descriptions import ArmToZeroDescription, LoadPaintDescription
from actionlib_msgs.msg import GoalStatusArray
import math
import moveit_commander
import rospy
import sys

_LOAD_X = (0.375, 0.475)

class ArmToZeroPrimitive(PrimitiveBase):
    def createDescription(self):
        self.setDescription(ArmToZeroDescription(), self.__class__.__name__)

    def onInit(self):
        moveit_commander.roscpp_initialize(sys.argv)
        self.mi_cmdr = moveit_commander.MoveGroupCommander('arm')
        rospy.Subscriber('/move_group/status', GoalStatusArray, self.feedback)

    def onStart(self):
        self.mi_cmdr.set_joint_value_target(self.mi_cmdr.get_named_target_values('zero'))
        self.mi_cmdr.go(wait=False)
        self.moving = True
        return True

    def execute(self):
        if self.moving:
            return self.step('Moving arm to zero position')
        return self.success('Finished moving arm to zero position')

    def onPreempt(self):
        self.mi_cmdr.stop()
        self.mi_cmdr.clear_pose_targets()
        return self.success('Moving arm to zero position preempted')

    def feedback(self, msg):
        self.moving = any(s.status in (0, 1) for s in msg.status_list)

class LoadPaintPrimitive(PrimitiveBase):
    def createDescription(self):
        self.setDescription(LoadPaintDescription(), self.__class__.__name__)

    def onInit(self):
        moveit_commander.roscpp_initialize(sys.argv)
        self.mi_cmdr = moveit_commander.MoveGroupCommander('arm')
        rospy.Subscriber('/move_group/status', GoalStatusArray, self.feedback)

    def onStart(self):
        targets = [[_LOAD_X[i % 2], 0, 0.05, -math.pi, 0, -math.pi] for i in range(self.params['passes'].value)]
        self.mi_cmdr.set_pose_targets(targets)
        self.mi_cmdr.go(wait=False)
        self.moving = True
        return True

    def execute(self):
        if self.moving:
            return self.step('Loading paint')
        return self.success('Finished loading paint')

    def onPreempt(self):
        self.mi_cmdr.stop()
        self.mi_cmdr.clear_pose_targets()
        return self.success('Loading paint preempted')

    # TODO: Need to check for when statuses change, not just existence of 0 or 1
    def feedback(self, msg):
        # The arm is moving if any goal statuses are 0 (PENDING) or 1 (ACTIVE)
        self.moving = any(s.status in (0, 1) for s in msg.status_list)
