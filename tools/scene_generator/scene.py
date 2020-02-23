#!/usr/bin/env python

import wall_sections

_PAINT_ROLLER_WIDTH = 0.2286
_WALL_SECTION_ID_START = 100

def gen_owl():
    print(wall_sections.gen_owl(
        (0, 0), (2, 0),
        _PAINT_ROLLER_WIDTH,
        'paintbot:Paint-1',
        _WALL_SECTION_ID_START))

# Test
gen_owl()
