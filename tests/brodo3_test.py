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
import sys
import os
path_to_script = os.path.dirname(os.path.abspath(__file__))
sys.path.append("/home/mjirik/projects/lar-cc/lib/py")


class TemplateTest(unittest.TestCase):

    def test_get_oriented_boundary(self):
        from larcc import VIEW, EXPLODE, MKPOLS, signedCellularBoundaryCells, AA, REVERSE, CAT
        V, FV, CV, VV, EV = gbmatrix.getBases(1, 2, 1)
        VIEW(EXPLODE(1.2, 1.2, 1.2)(MKPOLS((V,EV))))
        orientedBoundary = signedCellularBoundaryCells(V,AA(AA(REVERSE))([VV,EV,FV,CV]))
        cells = [FV[f] if sign==1 else REVERSE(FV[f]) for (sign,f) in zip(*orientedBoundary)]

        cells3 = CAT([[[v1, v2, v3], [v1, v3, v4]] for [v1, v2, v3, v4] in cells])
        cells3 = CAT([[[v1, v2, v3], [v3, v2, v4]] for [v1, v2, v3, v4] in cells])
        VIEW(EXPLODE(1.2, 1.2, 1.2)(MKPOLS((V,cells3))))
        import ipdb; ipdb.set_trace() #  noqa BREAKPOINT



    def test_getBases_correct_EV_len(self):
        V, FV, CV, VV, EV = gbmatrix.getBases(1, 2, 1)
        self.assertEqual(len(EV), 20)

if __name__ == "__main__":
    unittest.main()
