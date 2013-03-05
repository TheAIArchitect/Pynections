#!/usr/bin/python
'''
Created on Mar 4, 2013

@author: Andrew W.E. McDonald
'''

LOG_MODE = "debug"

def init_logger(name,log_mode="warning"):
    import logging
    logging.basicConfig(format="%(levelname)s - %(name)s:: %(message)s")
    log = logging.getLogger(name)
    if log_mode.__eq__("debug"):
        log.setLevel(logging.DEBUG)
    elif log_mode.__eq__("info"):
        log.setLevel(logging.INFO)
    return log