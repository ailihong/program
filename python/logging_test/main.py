#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 09:33:42 2019

@author: bai
"""

import json
import logging.config
import os
import subModule

def setup_logging(default_path = "logging.json",default_level = logging.INFO,env_key = "LOG_CFG"):
    path = default_path
    value = os.getenv(env_key,None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path,"r") as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level = default_level)

def func():
    
    logging.info("start func")

    logging.info("exec func")

    logging.info("end func")
       
        

if __name__ == "__main__":
    logger = logging.getLogger("mainModule")
    setup_logging(default_path = "logging.json")
    subModule.som_function()
    a = subModule.SubModuleClass()
    a.doSomething()
    func()
