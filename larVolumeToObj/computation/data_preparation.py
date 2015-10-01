#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import argparse

import sys

import io3d
import io3d.datareader
import io3d.datawriter
import sed3

def preparedata(inputfile, outputfile, crop=None, threshold=None):
    datap = io3d.datareader.read(inputfile, dataplus_format=True)
    if crop is not None:
        datap['data3d'] = datap['data3d'][crop[0][0]:crop[0][1], crop[1][0]:crop[1][1], crop[2][0]:crop[2][1]]
    if threshold is not None:
        datap['segmentation'] = datap['data3d'] > threshold
    ed = sed3.sed3(datap['data3d'], contour=datap['segmentation'])
    ed.show()
    # io3d.datawriter.write(datap, outputfile)
#



def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '%(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)
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
        description=__doc__
    )
    parser.add_argument(
        '-i', '--inputfile',
        default=None,
        required=True,
        help='input file'
    )
    parser.add_argument(
        '-o', '--outputfile',
        default='out.pklz',
        help='output file'
    )
    # parser.add_argument(
    #     '-bf', '--borderfile',
    #     default=None,
    #     help='input file'
    # )
    parser.add_argument(
        '-l', '--label',
        default=2,
        help='selected label or threshold for unlabeled data',
        type=int
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

    preparedata(args.inputfile, args.outputfile)


if __name__ == "__main__":
    main()
