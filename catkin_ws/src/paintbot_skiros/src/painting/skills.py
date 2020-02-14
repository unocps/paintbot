#!/usr/bin/env python

from descriptions import ApplyPaintDescription, LoadPaintDescription
from skiros2_skill.core.skill import SkillBase, Sequential

class LoadPaint(SkillBase):
    def createDescription(self):
        self.setDescription(LoadPaintDescription(), 'loadpaint')

    def set_relation(self, rel, src, dst, state):
        return self.skill('WmSetRelation', 'wm_set_relation',
            remap={'Dst': dst},
            specify={'Src': self.params[src].value, 'Relation': rel, 'RelationState': state})

    def expand(self, skill):
        self.setProcessor(Sequential())
        skill(
            self.skill('LoadPaintPrimitiveDescription', 'LoadPaintPrimitive'),
            self.skill('ArmToZeroPrimitiveDescription', 'ArmToZeroPrimitive'),
            self.set_relation('skiros:contain', 'PaintbotArm', 'PaintColor', True)
            # TODO: Remove previous color from arm
        )

class ApplyPaint(SkillBase):
    def createDescription(self):
        self.setDescription(ApplyPaintDescription(), 'applypaint')

    def set_relation(self, rel, src, dst, state):
        return self.skill('WmSetRelation', 'wm_set_relation',
            remap={'Dst': dst},
            specify={'Src': self.params[src].value, 'Relation': rel, 'RelationState': state})

    def expand(self, skill):
        self.setProcessor(Sequential())
        skill(
            self.skill('ApplyPaintPrimitiveDescription', 'ApplyPaintPrimitive'),
            self.skill('ArmToZeroPrimitiveDescription', 'ArmToZeroPrimitive'),
            self.set_relation('skiros:contain', 'Wall', 'PaintColor', True),
            # self.set_relation('skiros:contain', 'PaintbotArm', 'PaintColor', False)
        )
