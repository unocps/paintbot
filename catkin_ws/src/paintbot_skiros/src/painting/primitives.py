#!/usr/bin/env python

from actionlib_msgs.msg import GoalStatusArray
from descriptions import ApplyPaintPrimitiveDescription, ArmToZeroPrimitiveDescription, LoadPaintPrimitiveDescription
from moveit_msgs.msg import MoveGroupActionFeedback
from skiros2_common.core.primitive import PrimitiveBase
import math
import moveit_commander
import rospy
import sys

_LOAD_X = (0.375, 0.475)
_PAINT_Z = (0.4, 0.25)
_PASSES = 6

class ArmToZeroPrimitive(PrimitiveBase):
    def createDescription(self):
        self.setDescription(ArmToZeroPrimitiveDescription(), self.__class__.__name__)

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
        self.setDescription(LoadPaintPrimitiveDescription(), self.__class__.__name__)

    def onInit(self):
        moveit_commander.roscpp_initialize(sys.argv)
        self.mi_cmdr = moveit_commander.MoveGroupCommander('arm')
        rospy.Subscriber('/move_group/feedback', MoveGroupActionFeedback, self.feedback)

    def onStart(self):
        self.p = -1
        self.arm_fail = False
        self.move = True
        return True

    def execute(self):
        if self.arm_fail:
            return self.fail('Failed to load paint (unable to plan arm motion)', -1)

        if self.p < _PASSES:
            if self.move:
                self.mi_cmdr.set_pose_target([_LOAD_X[self.p % 2], 0, 0.05, -math.pi, 0, -math.pi])
                self.mi_cmdr.go(wait=False)
                self.move = False
            return self.step('Loading paint (pass {})'.format(self.p + 1))

        arm = self.params['Arm'].value
        arm.setRelation('-1', 'paintbot:hasColor', self.params['Paint'].value.id)
        self.params['Arm'].value = arm

        return self.success('Finished loading paint')

    def onPreempt(self):
        self.mi_cmdr.stop()
        self.mi_cmdr.clear_pose_targets()
        return self.success('Loading paint preempted')

    def feedback(self, msg):
        if msg.status.status == 3:
            self.p += 1
            self.move = True
        elif msg.status.status == 4:
            self.arm_fail = True

class ApplyPaintPrimitive(PrimitiveBase):
    def createDescription(self):
        self.setDescription(ApplyPaintPrimitiveDescription(), self.__class__.__name__)

    def onInit(self):
        moveit_commander.roscpp_initialize(sys.argv)
        self.mi_cmdr = moveit_commander.MoveGroupCommander('arm')
        # TODO: callback is being called in both primitives when only one is executing
        rospy.Subscriber('/move_group/feedback', MoveGroupActionFeedback, self.feedback)

    def onStart(self):
        self.p = -1
        self.arm_fail = False
        self.move = True
        return True

    def execute(self):
        if self.arm_fail:
            return self.fail('Failed to apply paint (unable to plan arm motion)', -1)

        if self.p < _PASSES:
            if self.move:
                self.mi_cmdr.set_pose_target([0.4, 0, _PAINT_Z[self.p % 2], 0, -math.pi / 2, math.pi])
                self.mi_cmdr.go(wait=False)
                self.move = False
            return self.step('Applying paint (pass {})'.format(self.p + 1))

        paint = self.params['Paint'].value
        wall = self.params['Wall'].value
        wall.setRelation('-1', 'paintbot:hasColor', paint.id)
        wall.setProperty('paintbot:Painted', 'Painted')
        self.params['Wall'].value = wall
        arm = self.params['Arm'].value
        arm.removeRelation(arm.getRelation('-1', 'paintbot:hasColor', paint.id))
        self.params['Arm'].value = arm

        return self.success('Finished applying paint')

    def onPreempt(self):
        self.mi_cmdr.stop()
        self.mi_cmdr.clear_pose_targets()
        return self.success('Applying paint preempted')

    def feedback(self, msg):
        if msg.status.status == 3:
            self.p += 1
            self.move = True
        elif msg.status.status == 4:
            self.arm_fail = True
