#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Generator of histology report

"""
import logging
logger = logging.getLogger(__name__)
import argparse
import sys

import numpy as np
# import traceback
import copy


def removeFromOneAxis():
    pass


def writeFile(filename, vertexes, faces):
    with open(filename, "w") as f:
        for vertex in vertexes:
            f.write("v %i %i %i\n" % (vertex[0], vertex[1], vertex[2]))

        for face in faces:
            fstr = "f "
            for i in range(0, len(face)):
                fstr += "%i " % (face[i])

            fstr += "\n"

            f.write(fstr)
            # f.write("f %i %i %i\n" % (face[0], face[1], face[2]))


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

    print isOnBoundary.shape
    print vertexes_axis.shape
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


def removeDoubleVertexesAndFaces(vertexes, faces):
    """
    Main function of module. Return object description cleand from double
    vertexes and faces.
    """

    new_vertexes, inv_vertexes = removeDoubleVertexes(vertexes)
    logger.info("Doubled vertex removed")
    logger.info("Number of vertexes: %i " % (len(new_vertexes)))
    new_faces = reindexVertexesInFaces(faces, inv_vertexes)
    logger.info("Faces reindexed")
    new_faces = removeDoubleFaces(new_faces)
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


def removeDoubleFaces(faces):
    """
    Return array of faces with remowed rows of both duplicates
    """
    faces_orig = copy.copy(np.array(faces))
    for face in faces:
        face = face.sort()
    faces = np.array(faces)

    b = np.ascontiguousarray(faces).view(
        np.dtype((np.void, faces.dtype.itemsize * faces.shape[1])))
    _, idx, inv = np.unique(b, return_index=True, return_inverse=True)
# now idx describes unique indexes
# but we want remove all duplicated indexes. Not only duplicates
    duplication_number = [np.sum(inv == i) for i in range(0, len(idx))]
    reduced_idx = idx[np.array(duplication_number) == 1]

    unique_faces = faces_orig[reduced_idx]
    return unique_faces.tolist()


def facesHaveAllPointsInList(faces, isOnBoundaryInds):
    faces = np.array(faces)
# Face has 3 points
    isInVoxelList = np.zeros(faces.shape, dtype=np.bool)
    for vertexInd in isOnBoundaryInds:
        isInVoxelList = isInVoxelList + (faces == vertexInd)

    suma = np.sum(isInVoxelList, 1)
    print 'sum ', np.max(suma)
    return suma >= 3


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
    import ipdb
    ipdb.set_trace()  # noqa BREAKPOINT
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
    v, f = removeDoubleVertexesAndFaces(v, f)
    writeFile('out.obj', v, f)
    print "After"
    print "Number of vertexes: %i    Number of faces %i" % (len(v), len(f))

if __name__ == "__main__":
    main(sys.argv)
