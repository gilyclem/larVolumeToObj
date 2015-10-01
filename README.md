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


Library
=======

    import larVolumeToObj
    import larVolumeToObj.computation
    import larVolumeToObj.computation as larobj
    larobj.pklzToSmoothObj.makeSmooth('nrn4.pklz', visualization=True)

More exaples
------------

    V, F = larobj.pklzToSmoothObj.makeSmooth('nrn4.pklz')
    larobj.visualization.visualize(V, F, explode=True)
    larobj.visualization.visualizeObj('output/out_sm_i_tr.obj', explode=True)



Commandline tools
=================


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
