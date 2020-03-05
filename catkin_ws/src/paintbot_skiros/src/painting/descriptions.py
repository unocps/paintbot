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
        self.addParam('Paint', Element('paintbot:Paint'), ParamTypes.Required)
        self.addParam('Arm', Element('rparts:ArmDevice'), ParamTypes.Inferred)

class ApplyPaintPrimitiveDescription(SkillDescription):
    def createDescription(self):
        self.addParam('Paint', Element('paintbot:Paint'), ParamTypes.Required)
        self.addParam('Wall', Element('paintbot:WallSection'), ParamTypes.Inferred)
        self.addParam('Arm', Element('rparts:ArmDevice'), ParamTypes.Inferred)

class GeneratePaintSubGoalPrimitiveDescription(SkillDescription):
    def createDescription(self):
        self.addParam('Goal', '', ParamTypes.Optional)

# Skills
class PaintAllWallSectionsDescription(SkillDescription):
    pass

class LoadPaintDescription(SkillDescription):
    def createDescription(self):
        self.addParam('Paint', Element('paintbot:Paint'), ParamTypes.Required)
        self.addParam('Tray', Element('paintbot:PaintTray'), ParamTypes.Inferred)
        self.addParam('Arm', Element('rparts:ArmDevice'), ParamTypes.Inferred)

        self.addPreCondition(ConditionRelation('NotArmHasColor', 'paintbot:hasColor', 'Arm', 'Paint', False))
        self.addPreCondition(ConditionRelation('TrayContainsColor', 'skiros:contain', 'Tray', 'Paint', True))
        self.addPreCondition(ConditionRelation('RobotAt', 'skiros:at', 'Robot', 'Tray', True))

        self.addHoldCondition(ConditionRelation('RobotAt', 'skiros:at', 'Robot', 'Tray', True))

        self.addPostCondition(ConditionRelation('ArmHasColor', 'paintbot:hasColor', 'Arm', 'Paint', True))

class ApplyPaintDescription(SkillDescription):
    def createDescription(self):
        self.addParam('Paint', Element('paintbot:Paint'), ParamTypes.Inferred)
        self.addParam('Wall', Element('paintbot:WallSection'), ParamTypes.Inferred)
        self.addParam('Arm', Element('rparts:ArmDevice'), ParamTypes.Inferred)

        self.addPreCondition(ConditionProperty('NotWallPainted', 'paintbot:Painted', 'Wall', '=', 'Painted', False))
        self.addPreCondition(ConditionRelation('WallTargetColor', 'paintbot:targetColor', 'Wall', 'Paint', True))
        self.addPreCondition(ConditionRelation('ArmHasColor', 'paintbot:hasColor', 'Arm', 'Paint', True))
        self.addPreCondition(ConditionRelation('RobotAtWall', 'skiros:at', 'Robot', 'Wall', True))

        self.addHoldCondition(ConditionRelation('RobotAtWall', 'skiros:at', 'Robot', 'Wall', True))

        self.addPostCondition(ConditionRelation('WallHasColor', 'paintbot:hasColor', 'Wall', 'Paint', True))
        self.addPostCondition(ConditionProperty('WallPainted', 'paintbot:Painted', 'Wall', '=', 'Painted', True))
        self.addPostCondition(ConditionRelation('PaintExpended', 'paintbot:hasColor', 'Arm', 'Paint', False))
