#!/usr/bin/env python

from descriptions import ApplyPaintDescription, LoadPaintDescription
from skiros2_skill.core.skill import SkillBase, Sequential

class LoadPaint(SkillBase):
    def createDescription(self):
        self.setDescription(LoadPaintDescription(), self.__class__.__name__)

    def expand(self, skill):
        self.setProcessor(Sequential())
        skill(
            self.skill('LoadPaintPrimitiveDescription', 'LoadPaintPrimitive'),
            self.skill('ArmToZeroPrimitiveDescription', 'ArmToZeroPrimitive')
        )

class ApplyPaint(SkillBase):
    def createDescription(self):
        self.setDescription(ApplyPaintDescription(), self.__class__.__name__)

    def expand(self, skill):
        self.setProcessor(Sequential())
        skill(
            self.skill('ApplyPaintPrimitiveDescription', 'ApplyPaintPrimitive'),
            self.skill('ArmToZeroPrimitiveDescription', 'ArmToZeroPrimitive')
        )
