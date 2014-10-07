#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import argparse

import sys
""" import modules from lar-cc/lib """
sys.path.insert(0, '/home/mjirik/projects/lar-cc/lib/py')
from larcc import *


# input of test file nrn100.py (with definetion of V and FV)
# V = vertex coordinates
# FV = lists of vertex indices of every face (1-based, as required by pyplasm)
#
# sys.path.insert(1, '/Users/paoluzzi/Documents/RICERCA/pilsen/ricerca/')
# from nrn100 import *


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

# scipy.sparse matrices required
# Computation of Vertex-to-vertex adjacency matrix
#


def adjacencyQuery(V, FV):
    # dim = len(V[0])
    csrFV = csrCreate(FV)
    csrAdj = matrixProduct(csrTranspose(csrFV), csrFV)
    return csrAdj


def adjacencyQuery0(dim, csrAdj, cell):
    nverts = 4
    cellAdjacencies = csrAdj.indices[
        csrAdj.indptr[cell]:csrAdj.indptr[cell + 1]]
    return [
        acell
        for acell in cellAdjacencies
        if dim <= csrAdj[cell, acell] < nverts
    ]


# construction of the adjacency graph of vertices
# returns VV = adjacency lists (list of indices of vertices
# adjacent to a vertex) of vertices
#
def adjVerts(V, FV):
    n = len(V)
    VV = []
    V2V = adjacencyQuery(V, FV)
    V2V = V2V.tocsr()
    for i in range(n):
        dataBuffer = V2V[i].tocoo().data
        colBuffer = V2V[i].tocoo().col
        row = []
        for val, j in zip(dataBuffer, colBuffer):
            if val == 2:
                row += [int(j)]
        VV += [row]
    return VV


def main():

    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    # logger.debug('input params')

    # input parser
    parser = argparse.ArgumentParser(
        description="Laplacian smoothing"
    )
    parser.add_argument(
        '-i', '--inputfile',
        default=None,
        required=True,
        help='input file'
    )
    parser.add_argument(
        '-o', '--outputfile',
        default='smooth.obj',
        help='input file'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    V, FV = readFile(args.inputfile)

    csrAdj = adjacencyQuery(V, FV)
# transformation of FV to 0-based indices (as required by LAR)
    FV = [[v - 1 for v in face] for face in FV]
    VIEW(STRUCT(MKPOLS((V, FV))))
    VIEW(EXPLODE(1.2, 1.2, 1.2)(MKPOLS((V, FV))))

    VV = adjVerts(V, FV)
# VIEW(STRUCT(MKPOLS((V,CAT([DISTR([VV[v],v ]) for v in range(n)]))))) #
# long time to evaluate

# Iterative Laplacian smoothing
# input V = initial positions of vertices
# output V1 = new positions of vertices
#
    V1 = AA(CCOMB)([[V[v] for v in adjs] for adjs in VV])

# input V1
# output V2 = new positions of vertices
#
    V2 = AA(CCOMB)([[V1[v] for v in adjs] for adjs in VV])
    VIEW(STRUCT(MKPOLS((V2, FV))))

if __name__ == "__main__":
    main()
