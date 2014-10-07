#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Generator of histology report

"""

import logging
logger = logging.getLogger(__name__)

import argparse
# import sys

import numpy as np
# import traceback
import copy
import time


def removeFromOneAxis():
    pass


def writeFile(filename, vertexes, faces):
    with open(filename, "w") as f:
        for vertex in vertexes:
            f.write("v %i %i %i\n" % (vertex[0], vertex[1], vertex[2]))

        for face in faces:
            fstr = "f"
            for i in range(0, len(face)):
                fstr += " %i" % (face[i])

            fstr += "\n"

            f.write(fstr)


def readFile(filename):
    vertexes = []
    faces = []
    with open(filename, "r") as f:
        for line in f.readlines():
            lnarr = line.strip().split(' ')
            if lnarr[0] == 'v':
                vertexes.append([
                    int(lnarr[1]),
                    int(lnarr[2]),
                    int(lnarr[3])
                ])
            if lnarr[0] == 'f':
                face = [0] * (len(lnarr) - 1)
                for i in range(1, len(lnarr)):
                    face[i - 1] = int(lnarr[i])
                faces.append(face)

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

    for coor in box_coordinates:
        isOnBoundary = isOnBoundary + (vertexes_axis == coor)

    return isOnBoundary


def reindexVertexesInFaces(faces, new_indexes):
    for face in faces:
        try:
            for i in range(0, len(face)):
                face[i] = new_indexes[face[i]-1] + 1
            # face[0] = new_indexes[face[0]-1] + 1
            # face[1] = new_indexes[face[1]-1] + 1
            # face[2] = new_indexes[face[2]-1] + 1
        except:
            import traceback
            traceback.print_exc()
            print 'fc ', face
            print len(new_indexes)

    return faces


def removeDoubleVertexesAndFaces(vertexes, faces, boxsize=None):
    """
    Main function of module. Return object description cleand from double
    vertexes and faces.
    """

    t0 = time.time()
    new_vertexes, inv_vertexes = removeDoubleVertexes(vertexes)
    t1 = time.time()
    logger.info("Doubled vertex removed          " + str(t1 - t0))
    logger.info("Number of vertexes: %i " % (len(new_vertexes)))
    new_faces = reindexVertexesInFaces(faces, inv_vertexes)
    t2 = time.time()
    logger.info("Vertexes in faces reindexed     " + str(t2 - t1))
    if boxsize is None:
        new_faces = removeDoubleFaces(new_faces)
    else:
        new_faces = removeDoubleFacesOnlyOnBoundaryBoxes(
            new_vertexes, new_faces, boxsize[0])
# @TODO add other axis
    t3 = time.time()
    logger.info("Double faces removed            " + str(t3 - t2))
    return new_vertexes, new_faces


def removeDoubleVertexes(vertexes):
    """
    Return array of faces with remowed rows of both duplicates
    """
    vertexes = np.array(vertexes)

    b = np.ascontiguousarray(vertexes).view(
        np.dtype((np.void, vertexes.dtype.itemsize * vertexes.shape[1])))
    _, idx, inv = np.unique(b, return_index=True, return_inverse=True)

    unique_vertexes = vertexes[idx]
    return unique_vertexes.tolist(), inv


def removeDoubleFacesOnlyOnBoundaryBoxes(vertexes, faces, bbsize):
    """
    Faster sister of removeDoubleFaces.

    It works only on box boundary
    """

    on, off = findBoundaryFaces(vertexes, faces, bbsize)

    # on = range(1, 100)

    off_boundary_faces = np.array(faces)[off]
    on_boundary_faces = np.array(faces)[on]
    new_on_boundary_faces = removeDoubleFaces(on_boundary_faces)
    new_faces = np.concatenate(
        (off_boundary_faces, np.array(new_on_boundary_faces)),
        0)
    return new_faces.tolist()


def removeDoubleFaces(faces):
    """
    Return array of faces with remowed rows of both duplicates
    """
    faces_orig = copy.copy(np.array(faces))
    for face in faces:
        face = face.sort()
    faces = np.array(faces)

    reduced_idx = getIndexesOfSingleFaces(faces)
    # reduced_idx2 = getIndexesOfSingleFacesBlocks(faces)
    # kimport ipdb; ipdb.set_trace() #  noqa BREAKPOINT

    unique_faces = faces_orig[reduced_idx]
    return unique_faces.tolist()


def getIndexesOfSingleFaces(faces):
    """
    Return indexes of not doubled faces.
    """
    b = np.ascontiguousarray(faces).view(
        np.dtype((np.void, faces.dtype.itemsize * faces.shape[1])))
    _, idx, inv = np.unique(b, return_index=True, return_inverse=True)
# now idx describes unique indexes
# but we want remove all duplicated indexes. Not only duplicates
    duplication_number = [np.sum(inv == i) for i in range(0, len(idx))]
    reduced_idx = idx[np.array(duplication_number) == 1]
    return reduced_idx


def getIndexesOfSingleFacesBlocks(faces):
    """
    Return indexes of not doubled faces.

    Function is sister of getIndexesOfSingleFaces. Difference is that
    computataion is performed by blocks
    """
    reduced_bool = np.zeros(faces.shape[0], dtype=np.bool)

    # working with whole list of faces is time consuming
    # this is why we do this in blocks
    block_size = 20
    for i in range(0, faces.shape[0]):
        # select faces with first
        selected = (faces[:, 0] >= i) * (faces[:, 0] < i + block_size)
        faces_subset = faces[selected]

        b = np.ascontiguousarray(faces_subset).view(
            np.dtype((np.void, faces.dtype.itemsize * faces_subset.shape[1])))
        _, idx, inv = np.unique(b, return_index=True, return_inverse=True)
# now idx describes unique indexes
# but we want remove all duplicated indexes. Not only duplicates
        duplication_number = [np.sum(inv == i) for i in range(0, len(idx))]
        subset_reduced_idx = idx[np.array(duplication_number) == 1]

        selected_idx_nz = np.nonzero(selected)
        selected_idx = selected_idx_nz[0]

        # arrange subset to original data
        reduced_bool[selected_idx[subset_reduced_idx]] = True
        reduced_idx = np.nonzero(reduced_bool)[0]
    return reduced_idx


def facesHaveAllPointsInList(faces, isOnBoundaryInds):
    faces = np.array(faces)
# Face has 3 points
    isInVoxelList = np.zeros(faces.shape, dtype=np.bool)
    for vertexInd in isOnBoundaryInds:
        isInVoxelList = isInVoxelList + (faces == vertexInd)

    suma = np.sum(isInVoxelList, 1)
    return suma >= faces.shape[1]


def findBoundaryFaces(vertexes, faces, step):
    """
    vertexes, step
    """

    # faces = np.array(faces)
    # print 'start ', faces.shape
    facesOnBoundary = np.zeros(len(faces), dtype=np.bool)
    for axis in range(0, 3):
        isOnBoundary = findBoundaryVertexesForAxis(
            vertexes, step, axis)
# faces.shape[1]
        isOnBoundaryInds = (np.nonzero(isOnBoundary)[0] + 1).tolist()
        facesOnBoundary += facesHaveAllPointsInList(faces, isOnBoundaryInds)


    # reduced faces set
    on_boundary = np.nonzero(facesOnBoundary)[0]
    off_boundary = np.nonzero(-facesOnBoundary)[0]
    # faces_new = faces[- facesOnBoundary]
    # print ' faces ', faces_new.shape
    # return vertexes, faces_new.tolist()
    return on_boundary, off_boundary


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

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
        default=None,
        type=int,
        metavar='N',
        nargs='+',
        help='Size of box'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    v, f = readFile(args.inputfile)
    print "Before"
    print "Number of vertexes: %i    Number of faces %i" % (len(v), len(f))
    # findBoxVertexesForAxis(v, 2, 0)
    # v, f = findBoundaryFaces(v, f, 2)
    v, f = removeDoubleVertexesAndFaces(v, f, args.boxsize)
    writeFile('out.obj', v, f)
    print "After"
    print "Number of vertexes: %i    Number of faces %i" % (len(v), len(f))

if __name__ == "__main__":
    main()
