#! /usr/bin/python
# -*- coding: utf-8 -*-

# import funkcí z jiného adresáře
import sys
import os.path

path_to_script = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path_to_script, "../py/computation/"))
import unittest

import step_remove_boxes_iner_faces as rmbox
import numpy as np


class HistologyTest(unittest.TestCase):
    interactiveTests = False

    #  @unittest.skipIf(not interactiveTests, "skipping ")
    def test_remove_double_faces(self):
        faces = [
            [1, 3, 6],
            [3, 2, 1],
            [4, 3, 1],
            [2, 1, 4],
            [1, 3, 2],
            [1, 3, 6]]

# sort all
        for face in faces:
            face = face.sort()

        faces_new = rmbox.removeDoubleFaces(faces)
        faces_new = np.array(faces_new)
        expected_faces = np.array([
            [1, 2, 4], [1, 3, 4]])

        self.assertAlmostEqual(0, np.sum(faces_new - expected_faces))

    def test_remove_vertexes(self):
        vertexes = [
            [1, 3, 6],
            [3, 2, 1],
            [3, 2, 1],
            [2, 1, 4],
            [1, 3, 5]]

        faces = [
            [0, 1, 3],
            [3, 2, 1],
            [4, 3, 1],
            [2, 0, 4],
            [1, 3, 2],
            [1, 3, 0]]

        expected_faces = np.array([
            [0, 1, 3], [0, 2, 3]])
        new_vertexes, inv_vertexes = rmbox.removeDoubleVertexes(vertexes)
        new_faces = rmbox.reindexVertexesInFaces(faces, inv_vertexes)
        faces_new = rmbox.removeDoubleFaces(new_faces)
        self.assertAlmostEqual(0, np.sum(faces_new - expected_faces))

if __name__ == "__main__":
    unittest.main()
