lar-running-demo
=============

A demo beta software (set of scripts) to extract models from medical images.
First step is image segmentation by Lisa software.

Spftware has been tested on Ubuntu 14.04 LTS (x64).

MIT License.


Install
-------

Install PyPlasm

Download LAR somewhere in your home directory. It will be found automatically.

    sudo apt-get install python-scipy python-numpy python-matplotlib\
        python-dicom

    pip install larVolumeToObj --user
    

Sample data
-----------

https://github.com/mjirik/lar-running-demo/blob/master/tests/nrn4.pklz


Library
-------

    import larVolumeToObj.computation as larobj
    V, F = larobj.pklzToSmoothObj.makeSmooth('nrn4.pklz')
    larobj.visualization.visualize(V,F, explode=True)

More exaples
============

    larobj.pklzToSmoothObj.makeSmooth('nrn4.pklz', visualization=True)
    larobj.visualization.visualizeObj('output/out_sm_i_tr.obj', explode=True)



volumeToObj.py
-------------

Extracts volume from pklz file or dicomdir

    python volumeToObj -i nrn4.pklz -od outdir -v


visualize.py
------------

Make visualization of objfile using Plasm

    python visualize.py -i outdir/out.obj


Usefull functions
-----------------



visualize.sh
-------------
Given a Wavefront STL model (*obj*) it will show it using available on system visualizers.

Supported visualizers: *PyPlasm, MeshLab, Manta*

Two type of executions:

* Interactive
* Command Line (use -h to know the exact paramaters)
