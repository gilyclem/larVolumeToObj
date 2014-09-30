#! /usr/bin/python
# -*- coding: utf-8 -*-

# import funkcí z jiného adresáře
import sys
import os.path

path_to_script = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path_to_script, "../py/computation/"))
import unittest

import smooth
import numpy as np


class SmoothingTest(unittest.TestCase):
    def test_smooth(self):
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
