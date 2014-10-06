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
            [1, 2, 4],
            [4, 3, 2],
            [5, 4, 2],
            [3, 1, 5],
            [2, 4, 3],
            [2, 4, 1]]

        expected_faces = np.array([
            [1, 2, 4], [1, 3, 4]])
        new_vertexes, inv_vertexes = rmbox.removeDoubleVertexes(vertexes)
        new_faces = rmbox.reindexVertexesInFaces(faces, inv_vertexes)
        faces_new = rmbox.removeDoubleFaces(new_faces)
        self.assertAlmostEqual(0, np.sum(faces_new - expected_faces))


    def test_face_have_all_points_in_list(self):
        faces = [
            [4, 1, 2, 3 ],
            [1, 4, 2, 5]
        ]
        isOnBoundary = [1, 2, 3, 4]

        fb = rmbox.facesHaveAllPointsInList(faces, isOnBoundary)
        self.assertItemsEqual(fb, [True, False])


    def test_findBoundaryFaces(self):
        v = [
            [10, 3, 3],
            [10, 4, 1],
            [10, 6, 2],
            [10, 6, 6],
            [8, 6, 6],
            [11, 8, 8],
        ]
        f = [
            [4, 1, 2, 3],
            [2, 4, 1, 6],
            [1, 4, 2, 5]
        ]

        on, off = rmbox.findBoundaryFaces(v, f, 10)
        self.assertItemsEqual(on, [0])
        self.assertItemsEqual(off, [1, 2])

    def test_real_data(self):
        vertexes, faces = rmbox.readFile("smallbb2.obj")
        new_vertexes, inv_vertexes = rmbox.removeDoubleVertexes(vertexes)
        new_faces = rmbox.reindexVertexesInFaces(faces, inv_vertexes)
        # new_faces = rmbox.removeDoubleFaces(new_faces)
        new_faces = rmbox.removeDoubleFacesOnlyOnBoundaryBoxes(
            new_vertexes, new_faces, 2)
        rmbox.writeFile('test_smallbb2_cleaned.obj', new_vertexes, new_faces)



if __name__ == "__main__":
    unittest.main()
