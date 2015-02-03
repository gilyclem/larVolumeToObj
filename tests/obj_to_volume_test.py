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


class TemplateTest(unittest.TestCase):

    def test_1_plus_1(self):
        self.assertEquals(1 + 1, 2)

    # @attr('interactive')
    def test_simple(self):
        import larVolumeToObj.computation.objToVolume as ov
        inputfile = "a008.rawc"

        ov.read_files_and_make_labeled_image(inputfile)


if __name__ == "__main__":
    unittest.main()
