#!/usr/bin/env python

import wall_section
import sys

_PAINT_ROLLER_WIDTH = 0.2286
_WALL_SECTION_ID_START = 100
_SCENE_OWL_TEMPLATE = """
@prefix paintbot: <http://unomaha.edu/ontologies/paintbot#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skiros: <http://rvmi.aau.dk/ontologies/skiros.owl#> .

skiros:Scene-0 rdf:type owl:NamedIndividual ,
        skiros:Scene ;
    #####
    # Tray contains go here
    #####
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

    #####
    # Other elements go here
    #####
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

    filename = sys.argv[1] if len(sys.argv) > 1 else 'room_paint_scene_1.turtle'
    with open(filename, 'w') as f:
        f.write(owl)

# Test
gen_owl((
    ((-2, -3), (-2, 0.5), 'paintbot:Paint-1'),
    ((4.5, -3.5), (-1.5, -3.5), 'paintbot:Paint-2')))
