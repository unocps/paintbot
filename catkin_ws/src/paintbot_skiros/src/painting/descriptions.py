#!/usr/bin/env python

from skiros2_common.core.params import ParamTypes
from skiros2_skill.core.skill import SkillDescription

# Primitives
class ArmToZeroPrimitiveDescription(SkillDescription):
    def createDescription(self):
        pass

class LoadPaintPrimitiveDescription(SkillDescription):
    def createDescription(self):
        self.addParam('passes', 6, ParamTypes.Required)

class ApplyPaintPrimitiveDescription(SkillDescription):
    def createDescription(self):
        self.addParam('passes', 6, ParamTypes.Required)

# Skills
class LoadPaintDescription(SkillDescription):
    def createDescription(self):
        self.addParam('passes', 6, ParamTypes.Required)

class ApplyPaintDescription(SkillDescription):
    def createDescription(self):
        self.addParam('passes', 6, ParamTypes.Required)
