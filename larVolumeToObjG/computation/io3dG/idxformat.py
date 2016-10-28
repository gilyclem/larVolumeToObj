#  /usr/bin/python
# -*- coding: utf-8 -*-

import os.path as op

import glob
import numpy as np
import os.path as op
import logging
logger = logging.getLogger(__name__)
import sed3

class IDXReader:
    def _init__(self):
        pass

    def read(self, datapath):
        import sys
	path_visuspy = '/media/cvdlab/1TBext4/nvisusio/build/linux'
	sys.path.append(path_visuspy)
	from visuspy import *
        app=Application()
	dataset=Dataset_loadDataset(datapath)

	logic_box=dataset.getLogicBox()
	field=Field("Ch1",DType("uint16"))
	access=dataset.createAccess()
    
	#box dimension
	box=NdBox(logic_box)
	box.setP1(0,500)
	box.setP1(1,500)
	box.setP1(2,500)
	box.setP2(0,600)
	box.setP2(1,600)
	box.setP2(2,550)
      
	#get the maximum resolution
	MaxH=dataset.getBitmask().getMaxResolution()
	print "MaxH = "
	print MaxH

	#perform the query
	query=Query(dataset,ord('r'))
	query.setLogicPosition(Position(box))
	query.setAccess(access)
	query.addEndResolution(MaxH)
	query.begin()
	query.execute()
	data3d=query.getBuffer().get().asNumPyArray()

	metadata = {} 
	metadata['series_number'] = 0  # reader.series_number
	metadata['datadir'] = datapath
	
        return data3d, metadata

    def read_files(self, datapath):

        dirp, filename = op.split(datapath)
        fn_template = op.join(dirp, self.header['filename_template'])

        fn_template = fn_template.replace("%04x", "????")
        filelist = glob.glob(fn_template.strip())
        filelist = sorted(filelist)
        print "sdfa"
        for fl in filelist:
            self.read_bin_file(fl, bitsperblock=int(self.header['bitsperblock']))
            pass

    def read_bin_file(self, filename, bitsperblock=8):
        bytesperblock = bitsperblock / 8
        if bytesperblock == 2:
            dtype = np.uint16
        else:
            logger.error("Unknown data type")

        data = np.fromfile(filename, dtype=np.uint8)
        shape = [1024, 1024, 10]
        d3 = np.reshape(data[:np.prod(shape)],shape)

        ed = sed3.sed3(d3[:200, :200, :])
        ed.show()
        print "all ok"


        # with open(filename, 'rb') as f:	# Use file to refer to the file object
        #
        #     data = f.read(bytesperblock)
        #


    def header_file_parser(self, datapath):
        self.file_keys = [
            'filename_template',
            'logic_to_physic',
            'bitsperblock',
            'blocksperfile',
            'interleave block',
            'box',
            'bits'
        ]
        if op.exists(datapath):
            logger.error("File '%s' not found" % (datapath))

        with open(datapath, 'rt') as f:	# Use file to refer to the file object
            data = f.readlines()
            # data = file.read()
            # print data

        out = {}
        for n, line in enumerate(data):
            line = data[n]
            for key in self.file_keys:
                if line.find("(" + key + ")") >= 0:
                    out[key] = data[n + 1]
        return out

class IDXWriter:
    def _init__(self):
        pass
