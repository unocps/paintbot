#!/usr/bin/env python

from skiros2_common.core.conditions import ConditionProperty, ConditionRelation
from skiros2_common.core.params import ParamTypes
from skiros2_common.core.world_element import Element
from skiros2_skill.core.skill import SkillDescription

# Primitives
class ArmToZeroPrimitiveDescription(SkillDescription):
    def createDescription(self):
        pass

class LoadPaintPrimitiveDescription(SkillDescription):
    def createDescription(self):
        self.addParam('Color', str, ParamTypes.Required)
        self.addParam('Arm', Element('rparts:ArmDevice'), ParamTypes.Inferred)

class ApplyPaintPrimitiveDescription(SkillDescription):
    def createDescription(self):
        self.addParam('Color', str, ParamTypes.Required)
        self.addParam('Wall', Element('paintbot:WallSection'), ParamTypes.Inferred)
        self.addParam('Arm', Element('rparts:ArmDevice'), ParamTypes.Inferred)

# Skills
class LoadPaintDescription(SkillDescription):
    def createDescription(self):
        self.addParam('Color', 'red', ParamTypes.Required)
        self.addParam('Paint', Element('paintbot:Paint'), ParamTypes.Inferred)
        self.addParam('Tray', Element('paintbot:PaintTray'), ParamTypes.Inferred)
        self.addParam('Arm', Element('rparts:ArmDevice'), ParamTypes.Inferred)

        self.addPreCondition(ConditionProperty('PaintIsColor', 'paintbot:Color', 'Paint', '=', 'red', True))
        self.addPreCondition(ConditionRelation('TrayContainsColor', 'skiros:contain', 'Tray', 'Paint', True))
        self.addPreCondition(ConditionRelation('RobotAt', 'skiros:at', 'Robot', 'Tray', True))

        self.addHoldCondition(ConditionRelation('RobotAt', 'skiros:at', 'Robot', 'Tray', True))

        self.addPostCondition(ConditionProperty('ArmHasColor', 'paintbot:Color', 'Arm', '=', 'red', True))

class ApplyPaintDescription(SkillDescription):
    def createDescription(self):
        self.addParam('Color', 'red', ParamTypes.Required)
        self.addParam('Wall', Element('paintbot:WallSection'), ParamTypes.Inferred)
        self.addParam('Arm', Element('rparts:ArmDevice'), ParamTypes.Inferred)

        self.addPreCondition(ConditionProperty('ArmHasColor', 'paintbot:Color', 'Arm', '=', 'red', True))
        self.addPreCondition(ConditionRelation('RobotAtWall', 'skiros:at', 'Robot', 'Wall', True))

        self.addHoldCondition(ConditionProperty('ArmHasColor', 'paintbot:Color', 'Arm', '=', 'red', True))
        self.addHoldCondition(ConditionRelation('RobotAtWall', 'skiros:at', 'Robot', 'Wall', True))

        self.addPostCondition(ConditionProperty('WallHasColor', 'paintbot:Color', 'Wall', '=', 'red', True))
        # self.addPostCondition(ConditionProperty('PaintExpended', 'paintbot:Color', 'Arm', '=', 'red', False))
