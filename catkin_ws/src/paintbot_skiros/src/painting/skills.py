#!/usr/bin/env python

from descriptions import ApplyPaintDescription, LoadPaintDescription
from skiros2_skill.core.skill import SkillBase, Sequential

class LoadPaint(SkillBase):
    def createDescription(self):
        self.setDescription(LoadPaintDescription(), 'loadpaint')

    def set_properties(self, src, properties):
        return self.skill('WmSetProperties', 'wm_set_properties',
            specify={'Src': self.params[src].value, 'Properties': properties})

    def expand(self, skill):
        self.setProcessor(Sequential())
        skill(
            self.skill('LoadPaintPrimitiveDescription', 'LoadPaintPrimitive'),
            self.set_properties('Arm', {'paintbot:Color': self.params['Color'].value}),
            # self.set_properties('Wall', {'paintbot:Color': -1}),
            self.skill('ArmToZeroPrimitiveDescription', 'ArmToZeroPrimitive')
        )

class ApplyPaint(SkillBase):
    def createDescription(self):
        self.setDescription(ApplyPaintDescription(), 'applypaint')

    def set_properties(self, src, properties):
        return self.skill('WmSetProperties', 'wm_set_properties',
            specify={'Src': self.params[src].value, 'Properties': properties})

    def expand(self, skill):
        self.setProcessor(Sequential())
        skill(
            self.skill('ApplyPaintPrimitiveDescription', 'ApplyPaintPrimitive'),
            self.set_properties('Wall', {'paintbot:Color': self.params['Color'].value}),
            self.skill('ArmToZeroPrimitiveDescription', 'ArmToZeroPrimitive')
        )
