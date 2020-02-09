#!/usr/bin/env python

from skiros2_common.core.conditions import ConditionRelation
from skiros2_common.core.params import ParamTypes
from skiros2_common.core.world_element import Element
from skiros2_skill.core.skill import SkillDescription

class NavigateToWallPrimitiveDescription(SkillDescription):
    def createDescription(self):
        self.addParam('Start', Element('skiros:Location'), ParamTypes.Inferred)
        self.addParam('Destination', Element('skiros:Location'), ParamTypes.Required)

        self.addPreCondition(ConditionRelation('RobotAt', 'skiros:at', 'Robot', 'Start', True))

        self.addPostCondition(ConditionRelation('RobotNotAt', 'skiros:at', 'Robot', 'Start', False))
        self.addPostCondition(ConditionRelation('RobotAt', 'skiros:at', 'Robot', 'Destination', True))
