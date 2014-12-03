#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 mjirik <mjirik@mjirik-Latitude-E6520>
#
# Distributed under terms of the MIT license.

"""
Module generate volumetric data from obj file
"""

import logging
logger = logging.getLogger(__name__)
import argparse
from fileio import readFile, writeFile
from scipy.spatial import Delaunay
import numpy as np

def read_files_and_make_labeled_image(filesmask):
    int_multiplicator = 1000
    data_offset = [5600,700,100]
    size = [300, 300, 300]

    Vraw, Fraw = readFile(filesmask)
    
    V = np.asarray(Vraw)
# TODO rozpracovat do obecnější formy
    #low number of unique numbers in axix - axis of slices
    # slice_axis = argmin  pro kazdou osu z:   len(np.unique(VVV[:,1]))
    slice_axis = 2

# TODO use this instead of fallowing fasthack - to be sure not loosing information
    #unV, invV = np.unique(V[:, 2], return_inverse=True)
    
    # ugly hack
    unV2 = np.unique(V[:, slice_axis])
    difV2 = unV2[1] - unV2[0]
    V[:, 2] = V[:, 2] / difV2


    # not nice discretization
    V[:, 0] = V [:, 0] * int_multiplicator
    V[:, 1] = V [:, 1] * int_multiplicator 


    Vint = V.astype(np.int) - data_offset


    for slicelevel in np.unique(Vint[:, 2]):
        selected = Vint[Vint[:, 2] == slicelevel, :]
        import ipdb; ipdb.set_trace() #  noqa BREAKPOINT

        




    import ipdb; ipdb.set_trace() #  noqa BREAKPOINT


def main():
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    # create file handler which logs even debug messages
    # fh = logging.FileHandler('log.txt')
    # fh.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(
    #     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)
    # logger.debug('start')

    # input parser
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    parser.add_argument(
        '-i', '--inputfile',
        default=None,
        required=True,
        help='input file'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    args = parser.parse_args()

    if args.debug:
        ch.setLevel(logging.DEBUG)

    read_files_and_make_labeled_image(args.inputfile)


if __name__ == "__main__":
    main()
