#!/usr/bin/env python

import math

_WALL_SECTION_OWL_TEMPLATE = """
paintbot:WallSection-{} rdf:type owl:NamedIndividual ,
        paintbot:WallSection ;
    skiros:OrientationX "{}"^^xsd:float ;
    skiros:OrientationY "{}"^^xsd:float ;
    skiros:OrientationZ "{}"^^xsd:float ;
    skiros:OrientationW "{}"^^xsd:float ;
    skiros:PositionX "{}"^^xsd:float ;
    skiros:PositionY "{}"^^xsd:float ;
    rdfs:label "Wall_{}"^^xsd:string ;
    paintbot:targetColor {} .
"""

def euler_to_quaternion(r, p, y):
    qx = math.sin(r/2) * math.cos(p/2) * math.cos(y/2) - math.cos(r/2) * math.sin(p/2) * math.sin(y/2)
    qy = math.cos(r/2) * math.sin(p/2) * math.cos(y/2) + math.sin(r/2) * math.cos(p/2) * math.sin(y/2)
    qz = math.cos(r/2) * math.cos(p/2) * math.sin(y/2) - math.sin(r/2) * math.sin(p/2) * math.cos(y/2)
    qw = math.cos(r/2) * math.cos(p/2) * math.cos(y/2) + math.sin(r/2) * math.sin(p/2) * math.sin(y/2)
    return [qx, qy, qz, qw]

def gen_wall_centers(p1, p2, width):
    # Normalized wall vector
    w = (p2[0] - p1[0], p2[1] - p1[1])
    w_mag = math.sqrt(w[0]**2 + w[1]**2)
    w = (w[0] / w_mag, w[1] / w_mag)
    # Calculate section centers
    num_secs = math.ceil(w_mag / width)
    sec_width = w_mag / num_secs
    centers = []
    for n in range(1, num_secs + 1):
        d = (n * sec_width) - (sec_width / 2)
        # Clamp d
        if d - (width / 2) < 0:
            d += (width / 2) - (sec_width / 2)
        elif d + (width / 2) > w_mag:
            d -= (width / 2) - (sec_width / 2)
        centers.append(((w[0] * d) + p1[0], (w[1] * d) + p1[1]))
    return centers

def gen_owl(p1, p2, width, target_color, id_start):
    # Note: Orientation of sections is theta(p2-p1) - math.pi/2
    centers = gen_wall_centers(p1, p2, width)
    id = id_start
    owl = ''
    for c in centers:
        q = euler_to_quaternion(0, 0, math.atan2(c[1], c[0]) - (math.pi / 2))
        owl += _WALL_SECTION_OWL_TEMPLATE.format(
            id,
            q[0], q[1], q[2], q[3],
            c[0], c[1],
            id - id_start,
            target_color)
        id += 1
    return owl
