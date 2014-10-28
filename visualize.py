#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import argparse

import sys
import os
""" import modules from lar-cc/lib """
sys.path.insert(0, os.path.expanduser('~/projects/lar-cc/lib/py'))
path_to_script = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path_to_script, "./py/computation/"))

from larcc import * # noqa
from fileio import readFile


# input of test file nrn100.py (with definetion of V and FV)
# V = vertex coordinates
# FV = lists of vertex indices of every face (1-based, as required by pyplasm)
#
# sys.path.insert(1, '/Users/paoluzzi/Documents/RICERCA/pilsen/ricerca/')
# from nrn100 import *


def triangulateSquares(F,
                       a=[0, 1, 2], b=[2, 3, 0],
                       c=[1, 0, 2], d=[3, 2, 0]
                       ):
    """
    Convert squares to triangles
    """
    FT = []
    for face in F:
        FT.append([face[a[0]], face[a[1]], face[a[2]]])
        FT.append([face[b[0]], face[b[1]], face[b[2]]])
        # FT.append([face[c[0]], face[c[1]], face[c[2]]])
        # FT.append([face[d[0]], face[d[1]], face[d[2]]])
        # FT.append([face[0], face[3], face[2]])
    return FT


# scipy.sparse matrices required
# Computation of Vertex-to-vertex adjacency matrix
#

def visualize(V, FV, explode=False):
    import time
    # VIEW(STRUCT(MKPOLS((V, FV))))
    t0 = time.time()
    mkpols = MKPOLS((V, FV))
    t1 = time.time()
    logger.debug("MKPOLS() done in %ss" % (str(t1 - t0)))
    if explode:
        VIEW(EXPLODE(1.2, 1.2, 1.2)(mkpols))
    else:
        struct = STRUCT(mkpols)
        t2 = time.time()
        logger.debug("STRUCT() done in %ss" % (str(t2 - t1)))
        VIEW(struct)


def visualize_plasm(V, FV):
    # import ipdb; ipdb.set_trace() #  noqa BREAKPOINT
    if len(FV[0]) > 3:
        FV = triangulateSquares(FV)
    logger.debug("triangulation done")

    FV1 = (np.asarray(FV) + 1).tolist()
    logger.debug(" + 1 done")
    VIEW(MKPOL([V, FV1, []]))
    # VIEW(MKPOL([V, AA(AA(lambda k:k + 1))(FV), []]))


def main():

    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    # logger.debug('input params')

    # input parser
    parser = argparse.ArgumentParser(
        description="Obj file visualization"
    )
    parser.add_argument(
        '-i', '--inputfile',
        default=None,
        required=True,
        help='input file'
    )
    parser.add_argument(
        '-ft', '--filetype',
        default='auto',
        help='filetype'
    )
    parser.add_argument(
        '-v', '--visualization', action='store_true',
        help='Use visualization')
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')

    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    V, FV = readFile(args.inputfile, ftype=args.filetype)

    logger.info("Data readed from ' %s" % (args.inputfile))
    visualize_plasm(V, FV)

if __name__ == "__main__":
    main()
