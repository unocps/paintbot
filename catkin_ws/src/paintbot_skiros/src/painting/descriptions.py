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
        pass

class ApplyPaintPrimitiveDescription(SkillDescription):
    def createDescription(self):
        pass

# Skills
class LoadPaintDescription(SkillDescription):
    def createDescription(self):
        self.addParam('PaintColor', Element('paintbot:Paint'), ParamTypes.Required)
        self.addParam('Tray', Element('paintbot:PaintTray'), ParamTypes.Inferred)
        self.addParam('PaintbotArm', Element('rparts:ArmDevice'), ParamTypes.Inferred)

        self.addPreCondition(ConditionRelation('TrayContainsColor', 'skiros:contain', 'Tray', 'PaintColor', True))
        self.addPreCondition(ConditionRelation('RobotAt', 'skiros:at', 'Robot', 'Tray', True))

        self.addHoldCondition(ConditionRelation('RobotAt', 'skiros:at', 'Robot', 'Tray', True))

        self.addPostCondition(ConditionRelation('ArmHasColor', 'skiros:contain', 'PaintbotArm', 'PaintColor', True))

class ApplyPaintDescription(SkillDescription):
    def createDescription(self):
        self.addParam('PaintColor', Element('paintbot:Paint'), ParamTypes.Inferred)
        self.addParam('Wall', Element('paintbot:WallSection'), ParamTypes.Inferred)
        self.addParam('PaintbotArm', Element('rparts:ArmDevice'), ParamTypes.Inferred)

        self.addPreCondition(ConditionRelation('ArmHasColor', 'skiros:contain', 'PaintbotArm', 'PaintColor', True))
        self.addPreCondition(ConditionRelation('RobotAtWall', 'skiros:at', 'Robot', 'Wall', True))

        self.addHoldCondition(ConditionRelation('ArmHasColor', 'skiros:contain', 'PaintbotArm', 'PaintColor', True))
        self.addHoldCondition(ConditionRelation('RobotAtWall', 'skiros:at', 'Robot', 'Wall', True))

        self.addPostCondition(ConditionRelation('WallHasColor', 'skiros:contain', 'Wall', 'PaintColor', True))
        # self.addPostCondition(ConditionRelation('PaintExpended', 'skiros:contain', 'PaintbotArm', 'PaintColor', False))
