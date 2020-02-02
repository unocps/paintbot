#!/usr/bin/env python

from skiros2_common.core.params import ParamTypes
from skiros2_skill.core.skill import SkillDescription

# Primitives
class ArmToZeroDescription(SkillDescription):
    def createDescription(self):
        pass

class LoadPaintDescription(SkillDescription):
    def createDescription(self):
        self.addParam('passes', 6, ParamTypes.Required)

class ApplyPaintDescription(SkillDescription):
    def createDescription(self):
        self.addParam('passes', 6, ParamTypes.Required)

# Skills
class LoadPaintSkillDescription(SkillDescription):
    def createDescription(self):
        self.addParam('passes', 6, ParamTypes.Required)

class ApplyPaintSkillDescription(SkillDescription):
    def createDescription(self):
        self.addParam('passes', 6, ParamTypes.Required)
