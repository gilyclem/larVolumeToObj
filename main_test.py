import larVolumeToObjG
#con i dati del fegato
#larVolumeToObjG.computation.data_preparation.preparedata("./biodur_sample/", 'biodur_crop.pklz', crop=[[0, 50], [200, 250], [200, 250]], threshold=1400, label=1, morphology=True, savePng=False)
#V, F = larVolumeToObjG.computation.pklzToSmoothObj.makeSmooth('biodur_crop.pklz', bordersize=[5,5,5], label=1, smoothing=False)

#con soglia precedentemente applicata
#larVolumeToObjG.computation.data_preparation.preparedata("/home/cvdlab/giulia/larVolumeToObjLocal/dataJL-Cycle1/", 'veins.pklz', crop=[[0, 25], [0, 1000], [0, 1000]], threshold=14, label=1, morphology=True, savePng=True)

#vene partendo dalle tiff nere
#larVolumeToObjG.computation.data_preparation.preparedata("/home/cvdlab/1TBext4/Cycle0-modelloVecchio", 'veins.pklz', crop=[[0, 25], [0, 1000], [0, 1000]], threshold=225, label=1, morphology=True, savePng=True)
#V, F = larVolumeToObjG.computation.pklzToSmoothObj.makeSmooth('veins.pklz', bordersize=[25,25,25], label=1, smoothing=False)

#Read from IDX file
larVolumeToObjG.computation.data_preparation.preparedata("/media/cvdlab/1TBext4/3DNeurons15Sept2016_/3DNeurons15Sept2016_00001.idx", 'neurons.pklz', threshold=200, label=1, morphology=True, savePng=True)
V, F = larVolumeToObjG.computation.pklzToSmoothObj.makeSmooth('neurons.pklz', bordersize=[25,25,25], label=1, smoothing=False)
#larVolumeToObjG.computation.visualization.visualize(V, F, explode=False)
