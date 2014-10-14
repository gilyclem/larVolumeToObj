#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Generator of histology report

"""
import logging
logger = logging.getLogger(__name__)
import argparse
import sys
import os
path_to_script = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path_to_script, "./py/computation/"))

from fileio import readFile, writeFile

# import traceback

	#$PYBIN ./py/computation/step_calcchains_serial_tobinary_filter_proc_lisa.py\
        # -r -b $BORDER_DIR/$BORDER_FILE -x $BORDER_X -y $BORDER_Y -z $BORDER_Z\
        # -i $DIRINPUT -c $COLORS -d $CHAINCURR -q $BESTFILE -o $COMPUTATION_DIR_BIN
import step_calcchains_serial_tobinary_filter_proc_lisa as s2bin
import step_remove_boxes_iner_faces as rmbox
import laplacianSmoothing as ls


def convert(filename, boxsize):
    s_bin.main()
    pass


def makeAll(args):
    V, F = readFile(args.inputfile)
    print "Before"
    print "Number of vertexes: %i    Number of faces %i" % (len(V), len(F))
    # findBoxVertexesForAxis(v, 2, 0)
    # v, f = findBoundaryFaces(v, f, 2)
    V, F = rmbox.removeDoubleVertexesAndFaces(V, F, args.boxsize)
    writeFile(args.outputfile + "cl.obj", V, F)
    print "After"
    print "Number of vertexes: %i    Number of faces %i" % (len(V), len(F))
    V, F = ls.makeSmoothing(V, F)
    writeFile(args.outputfile + "sm.obj", V, F)
    return V, F

def main():
    logger = logging.getLogger()

    logger.setLevel(logging.WARNING)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    # logger.debug('input params')

    # input parser
    parser = argparse.ArgumentParser(
        description="Read pklz with Pyplasm and LAR"
    )
    parser.add_argument(
        '-i', '--inputfile',
        default=None,
        required=True,
        help='input file'
    )
    parser.add_argument(
        '-o', '--outputfile',
        default='out',
        help='output file'
    )
    parser.add_argument(
        '-l', '--label',
        default=2,
        help='input file'
    )
    parser.add_argument(
        '-bf', '--borderfile',
        default=None,
        help='input file'
    )
    parser.add_argument(
        '-bd', '--borderdir',
        default="tmp/border",
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

    if args.borderfile is None:
        args.borderfile = args.borderdir

    makeAll(args)


if __name__ == "__main__":
    main()
