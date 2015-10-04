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
import larVolumeToObj.computation.laplacianSmoothing as ls
import larVolumeToObj.computation.step_remove_boxes_iner_faces as rmbox
import larVolumeToObj.computation.fileio as fileio

from larVolumeToObj.computation.visualization import check_references
# import visualize
import larVolumeToObj.computation.pklzToSmoothObj as sc


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
        # os.path.join(path_to_script, 'test_smallbb2_cleaned.obj'),
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
        self.assertTrue(check_references(V, F))
        # visualize.visualize(V, F)
        # expected_vertex = np.array(
        # [1, 3, 5])
        # print V[32]
        # self.assertAlmostEqual(
        #     0, np.sum(V[32] - expected_vertex))

    def make_all_by_steps_test(self):
        # from larcc import VIEW, EXPLODE, MKPOLS
        from larVolumeToObj.computation.pklzToSmoothObj import convert, \
            makeCleaningAndSmoothing
        from larVolumeToObj.computation.fileio import readFile
        # from visualize import visualize

        from larVolumeToObj.computation.step_triangularmesh \
            import triangulate_quads
        import shutil

        outputdir = 'tests/tmptestmakeall'
        if os.path.exists(outputdir):
            shutil.rmtree(outputdir)

        inputfile = 'tests/nrn4.pklz'
        bordersize = [4, 2, 3]
        outputdir = outputdir
        outputfile = 'test_nrn4'
        borderdir = outputdir + '/border'

        convert(inputfile, bordersize, outputdir, borderdir=borderdir)
        V, F = readFile(os.path.join(outputdir, 'stl/model-2.obj'))
        F3 = triangulate_quads(F)
        # visualize(V, F3)
        # VIEW(EXPLODE(1.2, 1.2, 1.2)(MKPOLS((V, F3))))
        V, F = makeCleaningAndSmoothing(
            V, F,
            os.path.join(outputdir, outputfile))

        F3 = triangulate_quads(F)
        self.assertTrue(check_references(V, F3))
        # visualize(V, F3, explode=True)
        # VIEW(EXPLODE(1.2, 1.2, 1.2)(MKPOLS((V, F3))))

    @attr('actual')
    def test_real_pklz_data(self):
        import larVolumeToObj.computation.pklzToSmoothObj as sc
        import shutil
        from larVolumeToObj.computation.step_triangularmesh \
            import triangulate_quads
        from larVolumeToObj.computation.visualization import check_references
        # from larcc import VIEW, EXPLODE, MKPOLS
        outputdir = 'tests/tmptestpklz'
        if os.path.exists(outputdir):
            shutil.rmtree(outputdir)
        V, F = sc.makeSmooth(
            inputfile='tests/nrn4.pklz',
            bordersize=[4, 2, 3],
            outputdir=outputdir,
            outputfile='test_nrn4',
            visualization=False,
            borderdir=outputdir + '/border',
            label=2
            # borderdir='tmp/border'
        )
        F3 = triangulate_quads(F)
        self.assertTrue(check_references(V, F))
        self.assertTrue(check_references(V, F3))

    @attr('interactive')
    def test_real_pklz_data_visual(self):
        import larVolumeToObj.computation.pklzToSmoothObj as startConversion
        import shutil
        from larVolumeToObj.computation.step_triangularmesh \
            import triangulate_quads
        from larVolumeToObj.computation.visualization \
            import visualize, check_references
        # from larcc import VIEW, EXPLODE, MKPOLS
        outputdir = 'tests/tmptestpklz'
        if os.path.exists(outputdir):
            shutil.rmtree(outputdir)
        V, F = startConversion.makeSmooth(
            # inputfile='tests/nrn4.pklz',
            inputfile='biodur_055.pklz',
            # inputfile='/home/mjirik/Stažené/nrn4.pklz',
            bordersize=[4, 2, 3],
            outputdir=outputdir,
            outputfile='test_nrn4',
            visualization=False,
            borderdir=outputdir + '/border'
            # borderdir='tmp/border'
        )
        F3 = triangulate_quads(F)
        visualize(V, F3, explode=True)
        self.assertTrue(check_references(V, F))
        # VIEW(EXPLODE(1.2, 1.2, 1.2)(MKPOLS((V, F3))))

    def test_preparedata(self):
        import larVolumeToObj
        import larVolumeToObj.computation.data_preparation as dp
        # inputfile = "/home/mjirik/projects/lisa/sample_data/biodur_sample/"
        inputfile = 'tests/nrn4.pklz'
        # larobj.datapreparation.preparedata('biodur_055.pklz')
        dp.preparedata(inputfile, 'nrn4_crop.pklz', crop=[[1, 6], [1, 6], [1, 6]], threshold=4400, visualization=False)
        V, F = larVolumeToObj.computation.pklzToSmoothObj.makeSmooth('nrn4_crop.pklz')
        # dp.preparedata(inputfile, 'nrn4_crop.pklz', crop=[[1, 40], [200, 250], [200, 250]], threshold=1400)

    @unittest.skip("test requires biodu_sample data")
    def test_prepare_biodur_sample(self):
        import larVolumeToObj
        inputfile = "/home/mjirik/projects/lisa/sample_data/biodur_sample/"
        larVolumeToObj.computation.data_preparation.preparedata(inputfile, 'biodur_crop.pklz', crop=[[1, 25], [200, 225], [200, 225]], threshold=1400)
        V, F = larVolumeToObj.computation.pklzToSmoothObj.makeSmooth('biodur_crop.pklz', bordersize=[5,5,5])
        larVolumeToObj.computation.visualization.visualize(V, F, explode=False)


if __name__ == "__main__":
    unittest.main()
