#!/usr/bin/env python

import wall_section

_PAINT_ROLLER_WIDTH = 0.2286
_WALL_SECTION_ID_START = 100
_SCENE_OWL_TEMPLATE = """
skiros:Scene-0 rdf:type owl:NamedIndividual ,
        skiros:Scene ;
    ###
    # Tray OWL goes here
    ###
{}
    skiros:DiscreteReasoner "AauSpatialReasoner"^^xsd:string ;
    skiros:FrameId "map"^^xsd:string ;
    skiros:OrientationW "1.0"^^xsd:float ;
    skiros:OrientationX "0.0"^^xsd:float ;
    skiros:OrientationY "0.0"^^xsd:float ;
    skiros:OrientationZ "0.0"^^xsd:float ;
    skiros:PositionX "0.0"^^xsd:float ;
    skiros:PositionY "0.0"^^xsd:float ;
    skiros:PositionZ "0.0"^^xsd:float ;
    rdfs:label "Scene"^^xsd:string .
"""

def gen_owl(segments):
    wall_sections = []
    id_start = _WALL_SECTION_ID_START
    for seg in segments:
        sections = wall_section.gen_owl(
            seg[0], seg[1],
            _PAINT_ROLLER_WIDTH,
            seg[2],
            id_start)
        id_start += len(sections)
        wall_sections += sections
    contains = ('    skiros:contain {} ;'.format(ws[0]) for ws in wall_sections)
    owl = _SCENE_OWL_TEMPLATE.format('\n'.join(contains))
    for ws in wall_sections:
        owl += ws[1]

    print(owl)

# Test
gen_owl((
    ((0, 0), (1, 0), 'paintbot:Paint-1'),
    ((1, 0), (2, 0), 'paintbot:Paint-2')))
