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
from nose.plugins.attrib import attr
import sys
import os
path_to_script = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path_to_script, "../../lar-cc/lib/py"))


class TemplateTest(unittest.TestCase):

    @attr('interactive')
    def test_get_oriented_boundary(self):
        from larcc import VIEW, EXPLODE, MKPOLS,\
            AA, CAT, signedCellularBoundary, swap, VECTPROD, DIFF,\
            CCOMB, SUM, POLYLINE
        import scipy
        V, FV, CV, VV, EV = gbmatrix.getBases(1, 2, 1)
        VIEW(EXPLODE(1.2, 1.2, 1.2)(MKPOLS((V, EV))))
        # orientedBoundary = signedCellularBoundaryCells(
        #     V, AA(AA(REVERSE))([VV, EV, FV, CV]))
        # cells = [FV[f] if sign == 1 else REVERSE(FV[f])
        #          for (sign, f) in zip(*orientedBoundary)]

        # FV3=CAT([[[v1, v2, v3], [v1, v3, v4]] for [v1, v2, v3, v4] in cells])
        # VIEW(EXPLODE(1.2, 1.2, 1.2)(MKPOLS((V, FV3))))

        def orientedBoundaryCells(V, (VV, EV, FV, CV)):
            boundaryMat = signedCellularBoundary(V, [VV, EV, FV, CV])
            chainCoords = scipy.sparse.csc_matrix((len(CV), 1))
            for cell in range(len(CV)):
                chainCoords[cell, 0] = 1
            boundaryCells = list((boundaryMat * chainCoords).tocoo().row)
            orientations = list((boundaryMat * chainCoords).tocoo().data)
            return zip(orientations, boundaryCells)

        def normalVector(V, facet):
            v0, v1, v2 = facet[:3]
            return VECTPROD([DIFF([V[v1], V[v0]]), DIFF([V[v2], V[v0]])])
        import ipdb; ipdb.set_trace()  # noqa BREAKPOINT

        boundaryCellspairs = orientedBoundaryCells(V, [VV, EV, FV, CV])
# external normals to faces
        orientedBoundary = [FV[face] if sign > 0 else swap(FV[face])
                            for (sign, face) in boundaryCellspairs]
        normals = [normalVector(V, facet) for facet in orientedBoundary]
        facetCentroids = [CCOMB([V[v] for v in facet])
                          for facet in orientedBoundary]
        appliedNormals = [
            [centroid, SUM([centroid, normal])]
            for (centroid, normal) in zip(facetCentroids, normals)]
        normalVectors = AA(POLYLINE)(appliedNormals)

# decomposition of quads into oriented triangles
        orientedQuads = [[sign, FV[face]] if sign > 0 else [
            sign, swap(FV[face])] for (sign, face) in boundaryCellspairs]
        FVtriangles = CAT([
            [[v0, v1, v2], [v2, v1, v3]] if sign > 0
            else [[v0, v1, v2], [v0, v2, v3]]
            for (sign, [v0, v1, v2, v3]) in orientedQuads])

        VIEW(EXPLODE(1.2, 1.2, 1.2)(MKPOLS((V, FVtriangles)) + normalVectors))

    def test_getBases_correct_EV_len(self):
        V, FV, CV, VV, EV = gbmatrix.getBases(1, 2, 1)
        self.assertEqual(len(EV), 20)

if __name__ == "__main__":
    unittest.main()
