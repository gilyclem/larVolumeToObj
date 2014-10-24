#! /usr/bin/python
# -*- coding: utf-8 -*-

# import funkcí z jiného adresáře
# import sys
import os.path

path_to_script = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(path_to_script, "../py/computation/"))
# sys.path.append(os.path.join(path_to_script, "../"))
import unittest

from nose.plugins.attrib import attr
import numpy as np
import laplacianSmoothing as ls
import step_remove_boxes_iner_faces as rmbox
import fileio
# import visualize
import startConversion as sc


class CommonTest(unittest.TestCase):
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

    def test_real_data_per_partes(self):
        vertexes, faces = fileio.readFile(
            os.path.join(path_to_script, "smallbb2.obj")
        )
        vertexes, inv_vertexes = rmbox.removeDoubleVertexes(vertexes)
        faces = rmbox.reindexVertexesInFaces(faces, inv_vertexes)
        faces = rmbox.removeDoubleFacesByAlberto(faces)

        # visualize.visualize(vertexes, faces)

        # rmbox.writeFile(
        #     os.path.join(path_to_script, 'test_smallbb2_cleaned.obj'),
        #     vertexes, faces)
        smooth_vertexes = ls.iterativeLaplacianSmoothing(vertexes, faces)
        expected_vertex = np.array(
            [1, 3, 5])
        self.assertAlmostEqual(
            0, np.sum(smooth_vertexes[32] - expected_vertex))
        # visualize.visualize(smooth_vertexes, faces)

    def test_real_data(self):
        V, F = fileio.readFile(
            os.path.join(path_to_script, "smallbb2.obj")
        )
        V, F = sc.makeCleaningAndSmoothing(V, F)
        # visualize.visualize(V, F)
        # expected_vertex = np.array(
        #     [1, 3, 5])
        # print V[32]
        # self.assertAlmostEqual(
        #     0, np.sum(V[32] - expected_vertex))

    @attr('actual')
    def test_real_pklz_data(self):
        import startConversion
        F, V = startConversion.makeAll(
            inputfile='nrn4.pklz',
            bordersize=[3, 3, 3],
            outputdir='tests/testpklz',
            outputfile='test_nrn4',
            visualization=False,
            borderdir='tests/border'
        )
        pass

if __name__ == "__main__":
    unittest.main()
