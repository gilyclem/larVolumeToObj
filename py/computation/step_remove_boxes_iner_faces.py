#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Generator of histology report

"""
import logging
logger = logging.getLogger(__name__)
import argparse
from lar import *

from scipy import *
import json
import scipy
import numpy as np
import time as tm
import gc
import struct
import getopt
import sys
import os
import traceback
import logging


def removeFromOneAxis():
    pass


def writeFile(filename, vertexes, faces):
    with open(filename, "w") as f:
        for vertex in vertexes:
            f.write("v %i %i %i\n" % (vertex[0], vertex[1], vertex[2]))

        for face in faces:
            f.write("f %i %i %i\n" % (face[0], face[1], face[2]))

def readFile(filename):
    vertexes = []
    faces = []
    with open(filename, "r") as f:
        for line in f.readlines():
            lnarr = line.split(' ')
            if lnarr[0] == 'v':
                vertexes.append([
                    int(lnarr[1]),
                    int(lnarr[2]),
                    int(lnarr[3])
                ]
                )
            if lnarr[0] == 'f':
                faces.append([
                    int(lnarr[1]),
                    int(lnarr[2]),
                    int(lnarr[3])
                ]
                )
    return vertexes, faces


def findBoundaryVertexesForAxis(vertexes, step, axis, isOnBoundary=None):
    """
    Return bool array of same length as is number of vertexes. It is true when
    vertex on same index is on box edge.
    """

    vertexes = np.array(vertexes)
    mx = np.max(vertexes[:, axis])
    mn = np.min(vertexes[:, axis])
    if mn < 0:
        logger.error("minimum is lower then 0")

    box_coordinates = range(0, mx, step)

    vertexes_axis = vertexes[:, axis]
    if isOnBoundary is None:
        isOnBoundary = np.zeros(vertexes_axis.shape, dtype=np.bool)

    print isOnBoundary.shape
    print vertexes_axis.shape
    for coor in box_coordinates:
        isOnBoundary = isOnBoundary + (vertexes_axis == coor)

    return isOnBoundary


def facesHaveAllPointsInList(faces, isOnBoundaryInds):
    faces = np.array(faces)
# Face has 3 points
    isInVoxelList = np.zeros(faces.shape, dtype=np.bool)
    for vertexInd in isOnBoundaryInds:
        isInVoxelList = isInVoxelList + (faces == vertexInd)

    suma = np.sum(isInVoxelList, 1)
    print 'sum ', np.max(suma)
    return suma == 3


def findBoundaryFaces(vertexes, faces, step):
    """
    vertexes, step
    """

    faces = np.array(faces)
    print 'start ', faces.shape
    facesOnBoundary = np.zeros(len(faces), dtype=np.bool)
    for axis in range(0, 3):
        isOnBoundary = findBoundaryVertexesForAxis(
            vertexes, step, axis)

        isOnBoundaryInds = np.nonzero(isOnBoundary)[0]
        facesOnBoundary += facesHaveAllPointsInList(faces, isOnBoundaryInds)

        print 'bound sum ', np.sum(facesOnBoundary)

    # reduced faces set
    faces_new = faces[- facesOnBoundary]
    import ipdb; ipdb.set_trace() #  noqa BREAKPOINT
    print ' faces ', faces_new.shape
    return vertexes, faces_new.tolist()


def main(argv):
    logger = logging.getLogger()

    logger.setLevel(logging.WARNING)
    # ch = logging.StreamHandler()
    # logger.addHandler(ch)

    # logger.debug('input params')

    # input parser
    parser = argparse.ArgumentParser(
        description="Remove faces from file"
    )
    parser.add_argument(
        '-i', '--inputfile',
        default=None,
        required=True,
        help='input file'
    )
    parser.add_argument(
        '-b', '--boxsize',
        default=[2, 2, 2],
        type=int,
        metavar='N',
        nargs='+',
        help='Size of box'
    )
    args = parser.parse_args()
    v, f = readFile(args.inputfile)
    #findBoxVertexesForAxis(v, 2, 0)
    v, f = findBoundaryFaces(v,f , 2)
    writeFile('out.obj', v, f)
    print len(v)
    print len(f)

if __name__ == "__main__":
    main(sys.argv[1:])
