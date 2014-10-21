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
import py.computation.step_generatebordermtx as gbmatrix


class TemplateTest(unittest.TestCase):

    def test_getBases_correct_EV_len(self):
        V, FV, CV, VV, EV = gbmatrix.getBases(1, 2, 1)
        self.assertEqual(len(EV), 20)
        # import ipdb; ipdb.set_trace() #  noqa BREAKPOINT

if __name__ == "__main__":
    unittest.main()
