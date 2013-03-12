#!/usr/bin/python
'''
Created on Mar 4, 2013

@author: Andrew W.E. McDonald


'admin.py' is the administrator. Takes care of the global constants, logger mode,
'''


# General constants
LOG_MODE =  "debug" # warning,

# ConceptNet constants
EDGE_KEYS_IN_USE = ["start","end","rel","weight","score"]#"features","startLemmas","relLemmas","endLemmas","context","text","nodes","uri"] # just a guess / for testing
NUM_EDGES_TO_RETURN = 50 # just a guess / for testing

# Stanford CoreNLP constants 

# middleman constants
MAX_OFFSET = 3 # -1 means the whole length of the sentence.
MIN_SIMILARITY = 0.5

# gauntlet constants
BEST_PERCENTAGE = 100 # will return top BEST_PERCENTAGE% of sentences
MAX_RESULTS = 500 # MAX_RESULTS overrides BEST_PERCENTAGE as a cap, but if BEST_PERCENTAGE is less than MAX_RESULTS, then BEST_PERCENTAGE limits the results. As the sentence gets longer, the number of results increase almost exponentially. This is due to a naiive design, and should be fixed. 


def init_logger(name,log_mode="warning"):
    ''' The project wide logger. I don't know if this is the right way to set up a project wide logger,
    but, until I find out a more efficient way, this is the project wide logger.
    '''
    import logging
    logging.basicConfig(format="%(levelname)s - %(name)s:: %(message)s")
    log = logging.getLogger(name)
    if log_mode.__eq__("debug"):
        log.setLevel(logging.DEBUG)
    elif log_mode.__eq__("info"):
        log.setLevel(logging.INFO)
    return log

