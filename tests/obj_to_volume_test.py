#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 mjirik <mjirik@mjirik-Latitude-E6520>
#
# Distributed under terms of the MIT license.

"""

"""
import unittest
from nose.plugins.attrib import attr
import larVolumeToObj.computation.objToVolume as ov

class TemplateTest(unittest.TestCase):

    @attr('interactive')
    def test_(self):
        inputfile = "a008.rawc"

        ov.read_files_and_make_labeled_image(inputfile)
        pass

if __name__ == "__main__":
    unittest.main()
