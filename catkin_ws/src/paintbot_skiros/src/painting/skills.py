#!/usr/bin/env python

from skiros2_skill.core.skill import SkillBase, Sequential, SerialStar
from descriptions import ApplyPaintSkillDescription, LoadPaintSkillDescription

class LoadPaintSkill(SkillBase):
    def createDescription(self):
        self.setDescription(LoadPaintSkillDescription(), self.__class__.__name__)

    def expand(self, skill):
        self.setProcessor(Sequential())
        skill(
            self.skill('LoadPaintDescription', 'LoadPaintPrimitive'),
            self.skill('ArmToZeroDescription', 'ArmToZeroPrimitive')
        )

class ApplyPaintSkill(SkillBase):
    def createDescription(self):
        self.setDescription(ApplyPaintSkillDescription(), self.__class__.__name__)

    def expand(self, skill):
        self.setProcessor(Sequential())
        skill(
            self.skill('ApplyPaintDescription', 'ApplyPaintPrimitive'),
            self.skill('ArmToZeroDescription', 'ArmToZeroPrimitive')
        )
