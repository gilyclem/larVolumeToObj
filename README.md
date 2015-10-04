[![Build Status](https://travis-ci.org/mjirik/larVolumeToObj.svg?branch=master)](https://travis-ci.org/mjirik/larVolumeToObj)

lar-running-demo
=============

A demo beta software (set of scripts) to extract models from medical images.
First step is image segmentation by Lisa software.

Spftware has been tested on Ubuntu 14.04 LTS (x64).

MIT License.


Install
======

Install PyPlasm

Download LAR somewhere in your home directory. It will be found automatically.

    sudo apt-get install python-scipy python-numpy python-matplotlib\
        python-dicom cython python-pip

    pip install larVolumeToObj
    

Sample data
===========

https://github.com/mjirik/larVolumeToObj/blob/master/tests/nrn4.pklz?raw=true

http://147.228.240.61/queetech/sample-data/biodur_sample.zip

Library
=======

    import larVolumeToObj
    larVolumeToObj.computation.pklzToSmoothObj.makeSmooth('nrn4.pklz', visualization=True)

Another exaples
------------

    V, F = larVolumeToObj.computation.pklzToSmoothObj.makeSmooth('nrn4.pklz')
    larVolumeToObj.computation.visualization.visualize(V, F, explode=True)
    larVolumeToObj.computation.visualization.visualizeObj('output/out_sm_i_tr.obj', explode=True)

Prepare DICOM or pklz data
---------------

    import larVolumeToObj
    import larVolumeToObj.computation.data_preparation as dp
    dp.preparedata('tests/nrn4.pklz', 'nrn4_crop.pklz', crop=[[1, 6], [1, 6], [1, 6]], threshold=4400, visualization=True)



More complex example - prepare, smooth and show
-----------------------------------------------

    import larVolumeToObj
    larVolumeToObj.computation.data_preparation.preparedata(
        "./biodur_sample/",
        'biodur_crop.pklz',
        crop=[[1, 25], [200, 225], [200, 225]],
        threshold=1400)
    V, F = larVolumeToObj.computation.pklzToSmoothObj.makeSmooth(
        'biodur_crop.pklz',
        bordersize=[5, 5, 5])
    larVolumeToObj.computation.visualization.visualize(V, F, explode=False)

Commandline tools
=================


data_preparation.py
----------

Simple data preprocessing tool. Allows cropping and thresholding.

    python data_preparation.py -i "tests/nrn4.pklz" -o prepared.pklz -threshold 4000 --visualization

    python data_preparation.py -i "biodur_sample/" -o prepared_biodur.pklz -c 1 40 200 250 200 250 -t 1400
    
    python data_preparation.py --help
    


volumeToObj.py
------------

Extracts volume from pklz file or dicomdir

    python volumeToObj -i nrn4.pklz -od outdir -v


visualize.py
------------

Make visualization of objfile using Plasm

    python visualize.py -i outdir/out.obj

visualize.sh
-------------

Given a Wavefront STL model (*obj*) it will show it using available on system visualizers.

Supported visualizers: *PyPlasm, MeshLab, Manta*

Two type of executions:

* Interactive
* Command Line (use -h to know the exact paramaters)
