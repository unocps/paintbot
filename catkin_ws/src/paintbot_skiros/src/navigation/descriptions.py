#!/usr/bin/env python

from skiros2_common.core.conditions import ConditionRelation
from skiros2_common.core.params import ParamTypes
from skiros2_common.core.world_element import Element
from skiros2_skill.core.skill import SkillDescription

# Primitives
class NavigateToLocationPrimitiveDescription(SkillDescription):
    def createDescription(self):
        self.addParam('Destination', Element('skiros:Location'), ParamTypes.Required)

# Skills
class NavigateToLocationDescription(SkillDescription):
    def createDescription(self):
        self.addParam('Start', Element('skiros:Location'), ParamTypes.Inferred)
        self.addParam('Destination', Element('skiros:Location'), ParamTypes.Required)

        self.addPreCondition(ConditionRelation('RobotAtStart', 'skiros:at', 'Robot', 'Start', True))
        self.addPreCondition(ConditionRelation('RobotNotAtDest', 'skiros:at', 'Robot', 'Destination', False))

        self.addPostCondition(ConditionRelation('RobotNotAtStart', 'skiros:at', 'Robot', 'Start', False))
        self.addPostCondition(ConditionRelation('RobotAtDest', 'skiros:at', 'Robot', 'Destination', True))
