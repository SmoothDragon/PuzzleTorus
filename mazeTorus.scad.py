#!/usr/bin/env python3

'''
Two "C" shaped tori can slide into each other. After rotating one, another
slide can be done to entangle them further.
'''

import numpy as np

from solid import *
from solid.utils import *


def parseArguments():
    # Argument parsing
    import argparse
    parser = argparse.ArgumentParser(
        description='Generate SCAD for Puzzle Torus.')
    parser.add_argument('-l', action='store', default='30', dest='length',
        type=float, help='Diameter (in millimeters) of torus arm.')
    parser.add_argument('--gap', action='store', default='.5', dest='gap',
        type=float, help='Tolerance gap between pieces.')  # gap=.1 tight
    parser.add_argument('-n', action='store', default='100', dest='fn',
        type=int, help='Curvature parameter. Number of sides on circle.')
    return parser.parse_args()


def latitudePaths(
        block:'3D object, centered at origin. Rotated to create paths.',
        r:'Radius of torus arm and center hole.',
        gap:'Amount of surface decrease to allow movement', 
        nPaths:'Number of longitude paths around torus',
        segments:'Number of copies of "block" that are unioned to create a path',
        ):
    block = translate([r-gap,0,0])(block)
    long_paths = []
    for phi in np.linspace(0, 360, num=nPaths+1):
        cutter = rotate([0,phi,0])(block)
        cutter = translate([2*r,0,0])(cutter)
        pieces = [rotate([0,0,360*i/segments])(cutter) for i in range(segments)]
        long_paths.append(union()(pieces))
    return long_paths

def longitudePaths(
        block:'3D object, centered at origin. Rotated to create paths.',
        r:'Radius of torus arm and center hole.',
        gap:'Amount of surface decrease to allow movement', 
        nPaths:'Number of longitude paths around torus',
        segments:'Number of copies of "block" that are unioned to create a path',
        ):
    block = translate([r-gap,0,0])(block)
    pieces = [rotate([0,360*i/segments,0])(block) for i in range(segments)]
    longitude = union()(pieces)
    longitude = translate([2*r,0,0])(longitude)
    longitudes = [rotate([0,0,theta])(longitude) for theta in np.linspace(0, 360, nPaths+1)]
    return union()(*longitudes)

def mazeTorus(
        block:'3D object, centered at origin. Rotated to create paths.',
        r:'Radius of torus arm and center hole.',
        gap:'Amount of surface decrease to allow movement', 
        nPaths:'Number of longitude paths around torus',
        segments:'Number of copies of "block" that are unioned to create a path',
        ):
    torus = rotate_extrude(convexity=10)(translate([r*2, 0])(circle(r-gap)))
    final = torus - union()(longitudePaths(block=block, r=r, gap=gap, nPaths=nPaths, segments=segments))
    final = final - union()(latitudePaths(block=block, r=r, gap=gap, nPaths=nPaths, segments=segments))
    # Diagonal X cut to join two tori
    diag_cut = cube(3*r)
    diag_cut = rotate([45,0,0])(diag_cut)
    diag_cut = translate([0,0,-gap])(diag_cut)
    diag_cut += rotate([180,0,0])(diag_cut)
    final = final - diag_cut
    # Add nub that travels in track of other torus
    final += hull()(translate([-r-2*gap,0,0])(block), translate([-2*r,0,0])(block))
    # final += translate([-r-2*gap,0,0])(scale([.5,1,1])(sphere(3)))
    # Orient for printing
    final = rotate([0,-90,0])(final)
    final = translate([0,0,(2+.866)*r-gap])(final)
    # Intersect with upper half plane
    upper_half = translate([0,0,5*r])(cube(10*r,center=True))
    final = intersection()(final, upper_half)
    return final

def addBlock():
    '''Add a block in the maze on the ith longitude and jth latitude
    '''
    pass

if __name__ == '__main__':
    args = parseArguments()
    size = args.length
    fn = args.fn
    gap = args.gap
    groove = 1.5  # Width of bottom of groove

    block = cube(4, center=True)
    block = hull()(
            cube([2*groove,groove,groove],center=True),
            cube([gap,4*groove,groove], center=True),
            cube([gap,groove,4*groove], center=True))
    block = translate([gap/2,0,0])(block)
    final = mazeTorus(block=block, r=args.length/2, gap=gap, nPaths=8, segments=fn)
    print(scad_render(final, file_header=f'$fn={args.fn};'))
