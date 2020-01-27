#!/usr/bin/env python

from skiros2_common.core.params import ParamTypes
from skiros2_skill.core.skill import SkillDescription

class LoadPaintDescription(SkillDescription):
    def createDescription(self):
        self.addParam("Passes", 6, ParamTypes.Required)
