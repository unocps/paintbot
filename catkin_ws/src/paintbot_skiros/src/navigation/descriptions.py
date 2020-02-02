#!/usr/bin/env python

from skiros2_common.core.params import ParamTypes
from skiros2_skill.core.skill import SkillDescription

class NavigateToWallPrimitiveDescription(SkillDescription):
    def createDescription(self):
        self.addParam('wall_x', 0.0, ParamTypes.Required)
        self.addParam('wall_y', 0.0, ParamTypes.Required)
        self.addParam('wall_facing', 0.0, ParamTypes.Required)
