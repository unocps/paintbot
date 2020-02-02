#!/usr/bin/env python

from skiros2_skill.core.skill import SkillBase, SerialStar
from descriptions import LoadPaintSkillDescription

class LoadPaintSkill(SkillBase):
    def createDescription(self):
        self.setDescription(LoadPaintSkillDescription(), self.__class__.__name__)

    def expand(self, skill):
        self.setProcessor(SerialStar())
        skill(
            self.skill('LoadPaintDescription', 'LoadPaintPrimitive'),
            self.skill('ArmToZeroDescription', 'ArmToZeroPrimitive')
        )
