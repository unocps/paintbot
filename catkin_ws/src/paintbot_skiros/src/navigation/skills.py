#!/usr/bin/env python

from descriptions import NavigateToLocationDescription
from skiros2_skill.core.skill import SkillBase

class NavigateToLocation(SkillBase):
    def createDescription(self):
        self.setDescription(NavigateToLocationDescription(), 'navigatetolocation')

    def set_relation(self, src, rel, dst, state):
        return self.skill('WmSetRelation', 'wm_set_relation',
            remap={'Dst': dst},
            specify={'Src': self.params[src].value, 'Relation': rel, 'RelationState': state})

    def expand(self, skill):
        skill(
            self.skill('NavigateToLocationPrimitiveDescription', 'NavigateToLocationPrimitive'),
            self.set_relation('Robot', 'skiros:at', 'Start', False),
            self.set_relation('Robot', 'skiros:at', 'Destination', True)
        )
