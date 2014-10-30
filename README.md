lar-running-demo
=============

A demo beta software (set of scripts) to extract models from medical images.
First step is image segmentation by Lisa software.

Spftware has been tested on Ubuntu 14.04 LTS (x64).

MIT License.

Prerequisites
-------------
Every script check for its own prerequisites at the right time.
A list of them are:

* *NIX like OS (untested on Windows)
* Bash
* Python (*PyPlasm, SciPy, NumPy, Cython, pypng, simplejson or json, requests, termcolor, matplotlib*)


Install 
-------

    sudo apt-get install python-scipy python-numpy python-matplotlib\
        python-dicom

    pip install io3d --user

Library
-------

    import larVolumeToObj
    larVolumeToObj.computation.pklzToSmoothObj.makeSmooth('nrn4.pklz')


volumeToObj.py
-------------

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
