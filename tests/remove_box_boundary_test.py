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
import copy


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
        new_faces = rmbox.reindexVertexesInFaces(faces, inv_vertexes,
                                                 index_base=0)
        faces_new = rmbox.removeDoubleFaces(new_faces)
        self.assertAlmostEqual(0, np.sum(faces_new - expected_faces))

    def test_face_have_all_points_in_list(self):
        faces = [
            [4, 1, 2, 3],
            [1, 4, 2, 5]
        ]
        isOnBoundary = [1, 2, 3, 4]

        fb = rmbox.facesHaveAllPointsInList(faces, isOnBoundary)
        self.assertItemsEqual(fb, [True, False])

    def test_findBoundaryFacesIndexBase1(self):
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

        on, off = rmbox.findBoundaryFaces(v, f, 10, index_base=1)
        self.assertItemsEqual(on, [0])
        self.assertItemsEqual(off, [1, 2])

    def test_findBoundaryFacesIndexBase0(self):
        v = [
            [10, 3, 3],
            [10, 4, 1],
            [10, 6, 2],
            [10, 6, 6],
            [8, 6, 6],
            [11, 8, 8],
        ]
        f = [
            [3, 0, 1, 2],
            [1, 3, 0, 5],
            [0, 3, 1, 4]
        ]

        on, off = rmbox.findBoundaryFaces(v, f, 10, index_base=0)
        self.assertItemsEqual(on, [0])
        self.assertItemsEqual(off, [1, 2])

    def test_real_data(self):
        vertexes, faces = rmbox.readFile("smallbb2.obj")
        # faces = rmbox.shiftFaces(faces, -1)
        new_vertexes, inv_vertexes = rmbox.removeDoubleVertexes(vertexes)
        new_faces = rmbox.reindexVertexesInFaces(faces, inv_vertexes)
        # new_faces = rmbox.removeDoubleFaces(new_faces)
        new_faces = rmbox.removeDoubleFacesOnlyOnBoundaryBoxes(
            new_vertexes, new_faces, 2)
        # new_faces = rmbox.shiftFaces(new_faces, 1)
        rmbox.writeFile('test_smallbb2_cleaned.obj', new_vertexes, new_faces)

    @unittest.skipIf(False, "skipping ")
    def test_benchmark_removeDoubleFaces(self):
        """
        Benchmark removing double faces
        """
        import time
        from larcc import t, larCuboids, boundaryCells, Model, Struct
        from larcc import struct2lar
        from larcc import VIEW, EXPLODE, MKPOLS
        cubes = larCuboids([10, 10, 10], True)
        V = cubes[0]
        FV = cubes[1][-2]
        CV = cubes[1][-1]
        bcells = boundaryCells(CV, FV)
        BV = [FV[f] for f in bcells]
        # VIEW(EXPLODE(1.2, 1.2, 1.2)(MKPOLS((V, BV))))

        block = Model((V, BV))
        struct = Struct(10 * [block, t(10, 0, 0)])
        struct = Struct(10 * [struct, t(0, 10, 0)])
        struct = Struct(3 * [struct, t(0, 0, 10)])
        W, FW1 = struct2lar(struct)
        FW2 = copy.copy(FW1)

        # VIEW(EXPLODE(1.2,1.2,1.2)(MKPOLS((W,FW))))
        t0 = time.time()
        FWO1 = rmbox.removeDoubleFaces(FW1)
        t1 = time.time()
        print "normal ", t1 - t0
        t0 = time.time()
        FWO2 = rmbox.removeDoubleFacesByAlberto(FW2)
        t1 = time.time()
        print "alberto ", t1 - t0
        # import ipdb; ipdb.set_trace() #  noqa BREAKPOINT
        # VIEW(EXPLODE(1.2,1.2,1.2)(MKPOLS((W,FWO1))))
        # VIEW(EXPLODE(1.2,1.2,1.2)(MKPOLS((W,FWO2))))


if __name__ == "__main__":
    unittest.main()
