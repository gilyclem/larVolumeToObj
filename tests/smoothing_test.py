#! /usr/bin/python
# -*- coding: utf-8 -*-

# import funkcí z jiného adresáře
import sys
import os.path

path_to_script = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path_to_script, "../py/computation/"))
sys.path.append(os.path.join(path_to_script, "../"))
import unittest

import smooth
import numpy as np
import laplacianSmoothing as ls


class SmoothingTest(unittest.TestCase):
    def test_smooth_alberto(self):
        vertexes = np.array([
            [1, 3, 6],
            [2, 2, 5],
            [2, 2, 4],
            [2, 1, 6],
            [1, 3, 5]])

        faces = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [1, 3, 4],
            [3, 4, 1]])

        expected_vertex = np.array(
            [1.25, 2.75, 5.5])

        nv = ls.makeSmoothing(vertexes, faces)

        self.assertAlmostEqual(0, np.sum(nv[0] - expected_vertex))

    def test_smooth_alberto_new(self):
        # from larcc import MKPOLS, STRUCT, VIEW
        vertexes = [
            [4, 4, 5],
            [1, 3, 2],
            [2, 5, 1],
            [5, 6, 1],
            [6, 1, 2],
            [4, 1, 2],
            [1, 1, 1],
        ]

        faces = [
            [0, 2, 1],
            [0, 3, 2],
            [0, 4, 3],
            [4, 0, 5],
            [1, 5, 0],
            [6, 1, 5],
        ]

        expected_vertex = np.array(
            [4, 4, 5])

        # facesp = (np.asarray(faces) + 1).tolist()
        # VIEW(STRUCT(MKPOLS((vertexes, faces))))

        nv = ls.iterativeLaplacianSmoothing(vertexes, faces)

        # VIEW(STRUCT(MKPOLS((nv, faces))))
        self.assertAlmostEqual(0, np.sum(nv[0] - expected_vertex))

    def test_why_is_it_kicking_only_once_used_vertex(self):
        # @TODO why?
        # from larcc import MKPOLS, STRUCT, VIEW
        vertexes = [
            [4, 4, 5],
            [1, 3, 2],
            [2, 5, 1],
            [5, 6, 1],
            [6, 1, 2],
            [4, 1, 2],
            [1, 1, 1],
        ]

        faces = [
            [0, 2, 1],
            [0, 3, 2],
            [0, 4, 3],
            [4, 0, 5],
            [1, 5, 0],
            [6, 1, 5],
        ]

        # VIEW(STRUCT(MKPOLS((vertexes, faces))))

        nv = ls.iterativeLaplacianSmoothing(vertexes, faces) # noqa

        # VIEW(STRUCT(MKPOLS((nv, faces))))

    def test_clean_unused_vertexes(self):
        # @TODO finish the test
        vertexes = np.array([
            [1, 3, 6],
            [2, 2, 5],
            [2, 2, 4],
            [2, 1, 6],
            [1, 3, 5]])

        faces = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [1, 3, 4],
            [3, 4, 1]])

        nv = ls.makeSmoothing(vertexes, faces)
        print nv

    def test_smooth_mira(self):
        vertexes = np.array([
            [1, 3, 6],
            [2, 2, 5],
            [2, 2, 4],
            [2, 1, 6],
            [1, 3, 5]])

        faces = np.array([
            [1, 2, 3],
            [1, 2, 4],
            [2, 4, 5],
            [4, 5, 2]])

        expected_vertex = np.array(
            [1.6, 2.2, 5.2])

        new_vertex = smooth.smoothPositionOfVertex(vertexes, faces, 2)

        self.assertAlmostEqual(0, np.sum(new_vertex - expected_vertex))
if __name__ == "__main__":
    unittest.main()
