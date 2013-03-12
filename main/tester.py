'''
Created on Mar 7, 2013

@author: Andrew W.E. McDonald


This tests various things,
'''
import time

first = time.time()
time.sleep(2)
second = time.time()
print "elapsed = "+str((second-first))