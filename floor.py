from openscad import *
from dataclasses import dataclass
from math import hypot
import json

from roof_generator import roof_generator


@dataclass
class Roof:
    start: list[list[float]]
    end: list[list[float]]
    

@dataclass
class Floor:
    base: list[list[float]]
    roof: Roof


with open("figures.json") as file:
    figures = json.load(file)
    floors = {
        name: Floor(
            base=figure["base"],
            roof=Roof(
                start=figure["roof_start"],
                end=figure["roof_end"],
            )
        )
        for name, figure in figures.items()
    }

    
    
def build_floor(name, size, height, joint_height):
     floor = floors[name]
     
     base = (
        polygon(_polygon(floor.base, size))
        .linear_extrude(height)
     )
     
     joint = (
        build_joint(
            name, size, joint_height, 
            scale=0.5, clearance=1.0)
        .translate([0, 0, height])
     )
     
     return difference(base, joint)
     

def build_roof(name, size, height):
    floor = floors[name]
    return roof_generator(
        height,
        _polygon(floor.roof.start, size),
        _polygon(floor.roof.end, size),
        "mansard",
        N=30,
    )
     
     
def build_joint(name, size, height, scale=1.0, clearance=0.0):
    floor = floors[name]
    s = 1.0 - 0.3 * scale
    return (
       polygon(_polygon(floor.base, size, clearance + 0.5))
       .offset(0.5, fn=20)
       .linear_extrude(height / scale, scale=[s, s])
       .mirror([0, 0, 1])
    )
     
     
def _polygon(poly, size, clearance=0.0):
    poly_scaled = [
        [x * size/2, y * size/2]
        for x, y in poly
    ]
    return _resize(poly_scaled, clearance)


def _resize(poly, margin):
    if margin == 0.0:
        return poly
    poly = poly.copy()
    for i in range(len(poly)):
        i_next = (i + 1) % len(poly)
        x0, y0 = poly[i]
        x1, y1 = poly[i_next]
        dx = x1 - x0
        dy = y1 - y0
        n = hypot(dx, dy)
        nx = dy / n * margin
        ny = -dx / n * margin
        poly[i][0] += nx
        poly[i][1] += ny
        poly[i_next][0] += nx
        poly[i_next][1] += ny
    return poly

for i, n in enumerate(["full", "edge", "side"]):
    union(
        build_floor(n, 10, 5, 3),
        build_joint(n, 10, 5, clearance=1.3)
    ).translate([i * 20, 0, 0]).show()
    
    union(
        build_floor(n, 10, 5, 3),
        build_joint(n, 10, 5, clearance=1.3)
    ).translate([i * 20, 0, 15]).show()
    
    union(
        build_roof(n, 10, 5),
        build_joint(n, 10, 5, clearance=1.3)
    ).translate([i * 20, 0, 30]).show()