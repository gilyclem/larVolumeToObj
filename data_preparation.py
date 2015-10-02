#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)


import larVolumeToObj
import larVolumeToObj.computation
import larVolumeToObj.computation.data_preparation as dp

if __name__ == "__main__":
    dp.main()