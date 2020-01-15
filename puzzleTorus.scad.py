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
    parser.add_argument('--gap', action='store', default='1', dest='gap',
        type=float, help='Tolerance gap between pieces.')  # gap=.1 tight
    parser.add_argument('-n', action='store', default='256', dest='fn',
        type=int, help='Curvature parameter. Number of sides on circle.')
    return parser.parse_args()


def puzzleTorus(
    r:'Torus radius.',
    gap:'Gap between pieces.'
    ):
    cross_section = intersection()(
        circle(r - gap),
        square([r*r, r*np.sqrt(3)-gap*2], center=True)
        )
    cross_section = translate([r*2, 0])(cross_section)
    torus = rotate_extrude(convexity=10)(cross_section)
    bumb_notch = cube([r*8, r/1, r/1], center=True)
    bumb_notch = intersection()(
        rotate([45,0,0])(bumb_notch),
        )
    notch = cube([r*4, r*np.sqrt(3)+gap*2, r*2], center=True)
    notch = translate([-r*2, 0, r])(notch)
    cut_notch = cube([r*4, r*np.sqrt(3)/2+gap*2, r*2], center=True)
    cut_notch = translate([r*2, -r*np.sqrt(3)/4, 0])(cut_notch)
    cut_notch += translate([r*4,0,0])(bumb_notch)
    torus = torus - notch + intersection()(bumb_notch, torus) - cut_notch
    return torus



if __name__ == '__main__':
    args = parseArguments()
    size = args.length
    fn = args.fn

    final = puzzleTorus(r=args.length/2, gap = args.gap)
    print(scad_render(final, file_header=f'$fn={args.fn};'))
