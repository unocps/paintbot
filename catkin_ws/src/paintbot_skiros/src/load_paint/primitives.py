#!/usr/bin/env python

from skiros2_common.core.primitive import PrimitiveBase
from descriptions import LoadPaintDescription

class LoadPaintPrimitive(PrimitiveBase):
    def createDescription(self):
        self.setDescription(LoadPaintDescription(), self.__class__.__name__)

    def onInit(self):
        return True

    def onStart(self):
        self.p = 0
        # TODO: Log starting message?
        return True

    def execute(self):
        self.p += 1
        if self.p > self.params['Passes'].value:
            return self.success('Finished loading paint')
        return self.step('')

    def onPreempt(self):
        return self.success('Stopped loading paint')
