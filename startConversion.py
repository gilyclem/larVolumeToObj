#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Generator of histology report

"""
import logging
logger = logging.getLogger(__name__)
import argparse
# import sys
# import os
# path_to_script = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(path_to_script, "./py/computation/"))

# import traceback

# $PYBIN ./py/computation/step_calcchains_serial_tobinary_filter_proc_lisa.py\
# -r -b $BORDER_DIR/$BORDER_FILE -x $BORDER_X -y $BORDER_Y -z $BORDER_Z\
# -i $DIRINPUT -c $COLORS -d $CHAINCURR -q $BESTFILE -o $COMPUTATION_DIR_BIN
import os
import errno
import numpy as np
import shutil
# import py
# import py.computation
# from py.computation import step_remove_boxes_iner_faces
import py.computation.step_calcchains_serial_tobinary_filter_proc_lisa as s2bin
from py.computation.fileio import readFile, writeFile
# import step_calcchains_serial_tobinary_filter_proc_lisa as s2bin
import py.computation.step_remove_boxes_iner_faces as rmbox
import py.computation.step_generatebordermtx as gbmatrix
import laplacianSmoothing as ls
import visualize

import py.computation.step_squaremesh as sq


def convert(filename, bordersize=[2, 2, 2], output_dir='tmp/output'):
    bindir = os.path.join(output_dir, 'compbin')
    stldir = os.path.join(output_dir, 'stl')
    binfile = os.path.join(bindir, 'model-2.bin')
    stlfile = os.path.join(stldir, 'model-2.obj')

    shutil.rmtree(output_dir)
    mkdir_p(output_dir)
    mkdir_p(stldir)
    mkdir_p(bindir)

    nx, ny, nz = bordersize
    brodo3path = gbmatrix.getBrodo3Path(nx, ny, nz, './tmp/border')
    logger.debug("in convert()")
    s2bin.calcchains_main(
        nx=nx, ny=ny, nz=nz,
        calculateout=True,
        input_filename=filename,
        # BORDER_FILE='./tmp/border/bordo3_2-2-2.json',
        BORDER_FILE=brodo3path,
        # BORDER_FILE=border_file,
        DIR_O=bindir,
        # colors=,
        coloridx=2
        )
    logger.debug("calcchains_main finished")

    concatenate_files(
        bindir + "/*.bin",
        binfile)
    logger.debug("concatenate() finished")
    # nx, ny, nz = boxsize
    sq.make_obj(
        nx, ny, nz,
        binfile,
        stldir)
    logger.debug("obj file  finished")

    concatenate_files(stldir + '/output-*-*.stl', stlfile)


def makeAll(args):
    print 'before pklz read'
    convert(args.inputfile, args.bordersize)
    print 'after pklz read'
    # V, F = readFile(args.inputfile)
    V, F = readFile('tmp/output/stl/model-2.obj')
    print "Before"
    print "Number of vertexes: %i    Number of faces %i" % (len(V), len(F))
    # F = rmbox.shiftFaces(F, -1)
    V, F = makeCleaningAndSmoothing(V, F, args.outputfile)
    print "After"
    print "Number of vertexes: %i    Number of faces %i" % (len(V), len(F))

    if args.visualization:
        visualize.visualize(V, F)

    return V, F


def makeCleaningAndSmoothing(V, F, outputfile=None):
    # findBoxVertexesForAxis(v, 2, 0)
    # v, f = findBoundaryFaces(v, f, 2)
    V, F = rmbox.removeDoubleVertexesAndFaces(V, F, use_dict_algorithm=False)
    if outputfile is not None:
        writeFile(outputfile + "_cl.obj", V, F)
    V = ls.makeSmoothing(V, F)
    if outputfile is not None:
        writeFile(outputfile + "_sm.obj", V, F,
                  ignore_empty_vertex_warning=True)
        writeFile(outputfile + "_sm_i.obj",
                  (np.asarray(V) * 10).tolist(), F,
                  ignore_empty_vertex_warning=True)
    return V, F


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def concatenate_files(input_filemasc, output_filename):
    import glob

    read_files = glob.glob(input_filemasc)
    logger.debug('concatenate files')
    logger.debug(str(read_files))

    with open(output_filename, "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())
    logger.info("Files concatenated to '%s'" % (output_filename))


def main():
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('log.txt')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.debug('start')

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
        '-b', '--bordersize',
        default=[2, 2, 2],
        type=int,
        metavar='N',
        nargs='+',
        help='Size of box'
    )
    parser.add_argument(
        '-v', '--visualization', action='store_true',
        help='Visualization')
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    args = parser.parse_args()
    if args.debug:
        ch.setLevel(logging.DEBUG)

    if args.borderfile is None:
        args.borderfile = args.borderdir

    makeAll(args)


if __name__ == "__main__":
    main()
