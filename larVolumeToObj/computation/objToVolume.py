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
import glob
import re


def points_to_volume_3D(data3d, points):
    """
    Not fixed yet. Should be better then slice version
    """
    # hack move one point in next slice to make non planar object
    points[0, 2] += 1
    points[-1, 2] += -1


    hull = Delaunay(points)
    X, Y, Z = np.mgrid[:data3d.shape[0],:data3d.shape[1], :data3d.shape[2]]
    grid = np.vstack([X.ravel(), Y.ravel(), Z.ravel()]).T
    simplex = hull.find_simplex(grid)
    fill = grid[simplex >=0,:]
    fill = (fill[:,0], fill[:,1], fill[:,2])
    data3d[fill] = 1

def points_to_volume_slice(data3d, points, label):
    """
    Only planar points can be used
    """
    # hack move one point in next slice to make non planar object
    z = points[0, 2]
    points = points[:, :2]

    hull = Delaunay(points)
    X, Y = np.mgrid[:data3d.shape[0], :data3d.shape[1]]
    grid = np.vstack([X.ravel(), Y.ravel()]).T
    simplex = hull.find_simplex(grid)
    fill = grid[simplex >=0,:]
    fill = (fill[:,0], fill[:,1])
    # contours = np.zeros(data3d.shape, np.int8)
    # contours[fill] = 1
    data_slice = data3d[z, :, :]
    data_slice[fill] = label




def read_files_and_make_labeled_image(filesmask, data_offset=None, data_size=None):
    int_multiplicator = 70

    filenames = glob.glob(filesmask)
    if data_offset is None or data_size is None:
        data_offset, sz = find_bbox(filenames)

    # data_offset = [5600, 6900, 100]
# size cannot be estimated easily
    size = [300, 300, 300]
    data3d = np.zeros(size)
    for filename in filenames:
        try:
            read_one_file_add_to_labeled_image(filename, data3d, data_offset, int_multiplicator)
        except:
            import traceback
            logger.warning(traceback.format_exc())


    import sed3
    ed = sed3.sed3(data3d)
    ed.show()

def find_bbox(filenames):
    data_min=[]
    data_max = []
    for filename in filenames:
        Vraw, Fraw = readFile(filename)
        V = np.asarray(Vraw) 
        data_min.append(np.min(V, axis=0))
        data_max.append(np.max(V, axis=0))

    mx = np.max(V, axis=0)
    mi = np.min(V, axis=0)

    return mi, mx


def read_one_file_add_to_labeled_image(filename, data3d, data_offset, int_multiplicator):
    Vraw, Fraw = readFile(filename)

    # parse filename
    nums = re.findall(r'\d+', filename)
    label = int(nums[0])

    

    
    V = np.asarray(Vraw) 
    # data_offset = np.min(V, axis=0)
    V = V - data_offset

# TODO rozpracovat do obecnější formy
    #low number of unique numbers in axix - axis of slices
    # slice_axis = argmin  pro kazdou osu z:   len(np.unique(VVV[:,1]))
    slice_axis = 2

# TODO use this instead of fallowing fasthack - to be sure not loosing information
    unV2, invV2 = np.unique(V[:, 2], return_inverse=True)
    V[:,2] = invV2

    # not nice discretization
    V[:, 0] = V [:, 0] * int_multiplicator
    V[:, 1] = V [:, 1] * int_multiplicator 

    Vint = V.astype(np.int) # - data_offset

    for slicelevel in np.unique(Vint[:, 2]):
        points = Vint[Vint[:, 2] == slicelevel, :]
        t = False 

        if points.shape[0] > 2:
            points_to_volume_slice(data3d, points, label)
            # points_to_volume_3D(data3d, points)
        else:
            print "low number of points" , points.shape[0],\
                    " z-level ", points[0, 2]


        






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
