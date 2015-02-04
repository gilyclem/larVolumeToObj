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


class TemplateTest(unittest.TestCase):

    def test_import_lar(self):
        import sys

        import larVolumeToObj.computation.import_library as il
        lib_path = il.find_library_path("larcc", "larcc.py")
        sys.path.append(lib_path)
        from larcc import MKPOLS

if __name__ == "__main__":
    unittest.main()
