#!/usr/bin/env python

_PAINT_OWL_TEMPLATE = """
{} rdf:type owl:NamedIndividual ,
        paintbot:Paint ;
    rdfs:label "Paint_{}"^^xsd:string .
"""

_TRAY_OWL_TEMPLATE = """
{} rdf:type owl:NamedIndividual ,
        paintbot:PaintTray ;
    skiros:contain {} ;
    skiros:OrientationX "0"^^xsd:float ;
    skiros:OrientationY "0"^^xsd:float ;
    skiros:OrientationZ "-0.707"^^xsd:float ;
    skiros:OrientationW "0.707"^^xsd:float ;
    skiros:PositionX "{}"^^xsd:float ;
    skiros:PositionY "{}"^^xsd:float ;
    rdfs:label "PaintTray_{}"^^xsd:string .
"""

def generate(tray_loc, paint, paint_id, tray_id):
    paint_full_id = 'paintbot:Paint-{}'.format(paint_id)
    paint_owl = _PAINT_OWL_TEMPLATE.format(paint_full_id, paint)

    # TODO: Orientation
    tray_full_id = 'paintbot:PaintTray-{}'.format(tray_id)
    tray_owl = _TRAY_OWL_TEMPLATE.format(
        tray_full_id,
        paint_full_id,
        tray_loc[0], tray_loc[1],
        paint)

    return (paint_full_id, paint_owl), (tray_full_id, tray_owl)
