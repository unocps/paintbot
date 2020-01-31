#!/usr/bin/env python

from skiros2_common.core.primitive import PrimitiveBase
from descriptions import LoadPaintDescription
import math
import moveit_commander
import sys
import threading

_LOAD_X = (0.375, 0.475)

class LoadPaintPrimitive(PrimitiveBase):
    def createDescription(self):
        self.setDescription(LoadPaintDescription(), self.__class__.__name__)

    def onInit(self):
        moveit_commander.roscpp_initialize(sys.argv)
        self.mi_cmdr = moveit_commander.MoveGroupCommander('arm')

    def onStart(self):
        self.painting = True
        t = threading.Thread(target=self.load_paint)
        t.start()
        return True

    def execute(self):
        if self.painting:
            return self.step('Loading paint...')
        return self.success('Finished loading paint')

    def onPreempt(self):
        self.mi_cmdr.stop()
        self.mi_cmdr.clear_pose_targets()
        return self.success('Stopped loading paint')

    def move_arm_to_zero(self):
        self.mi_cmdr.set_joint_value_target(self.mi_cmdr.get_named_target_values('zero'))
        self.mi_cmdr.go(wait=True)
        self.mi_cmdr.stop()
        self.mi_cmdr.clear_pose_targets()

    def load_paint(self):
        for i in range(self.params['passes'].value):
            self.mi_cmdr.set_pose_target([_LOAD_X[i % 2], 0, 0.05, -math.pi, 0, -math.pi])
            self.mi_cmdr.go(wait=True)
            self.mi_cmdr.stop()
            self.mi_cmdr.clear_pose_targets()
        self.move_arm_to_zero()
        self.painting = False
