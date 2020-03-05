#!/usr/bin/env python

from descriptions import ApplyPaintDescription, LoadPaintDescription, PaintAllWallSectionsDescription
from skiros2_skill.core.skill import SkillBase, Sequential
import math

class PaintAllWallSections(SkillBase):
    def createDescription(self):
        self.setDescription(PaintAllWallSectionsDescription(), 'paintallwallsections')

    def expand(self, skill):
        skills = []
        unpainted = len([not self.wmi.get_element(i).hasProperty('Painted') for i in self.wmi.get_individuals('paintbot:WallSection')])
        for i in range(int(math.ceil(unpainted / 10.0))):
            skills.append(self.skill('GeneratePaintSubGoalPrimitiveDescription', 'GeneratePaintSubGoalPrimitive'))
            skills.append(self.skill('TaskPlan', 'task_plan'))

        skill(*skills)

class LoadPaint(SkillBase):
    def createDescription(self):
        self.setDescription(LoadPaintDescription(), 'loadpaint')

    def expand(self, skill):
        self.setProcessor(Sequential())
        skill(
            self.skill('LoadPaintPrimitiveDescription', 'LoadPaintPrimitive'),
            self.skill('ArmToZeroPrimitiveDescription', 'ArmToZeroPrimitive')
        )

class ApplyPaint(SkillBase):
    def createDescription(self):
        self.setDescription(ApplyPaintDescription(), 'applypaint')

    def expand(self, skill):
        self.setProcessor(Sequential())
        skill(
            self.skill('ApplyPaintPrimitiveDescription', 'ApplyPaintPrimitive'),
            self.skill('ArmToZeroPrimitiveDescription', 'ArmToZeroPrimitive')
        )
