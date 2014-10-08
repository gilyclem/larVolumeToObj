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

	#$PYBIN ./py/computation/step_calcchains_serial_tobinary_filter_proc_lisa.py\
        -r -b $BORDER_DIR/$BORDER_FILE -x $BORDER_X -y $BORDER_Y -z $BORDER_Z\
        -i $DIRINPUT -c $COLORS -d $CHAINCURR -q $BESTFILE -o $COMPUTATION_DIR_BIN
import step_calcchains_serial_tobinary_filter_proc_lisa as s_bin


def convert(filename, boxsize):
    argv =
    s_bin.main()
    pass

def main():
    logger = logging.getLogger()

    logger.setLevel(logging.WARNING)
    ch = logging.StreamHandler()
    # logger.addHandler(ch)

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

if __name__ == "__main__":
    main()
