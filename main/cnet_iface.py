#!/usr/bin/python
'''
Created on Feb 19, 2013

@author: Andrew W.E. McDonald
'''
from __future__ import division
import urllib2
import simplejson as json
import admin

log = admin.init_logger("cnet_iface", admin.LOG_MODE)


_base = "http://conceptnet5.media.mit.edu/data/5.1/"
_lang = "en"

node_type = ["concept","frame","relation","assertion","sense"]
edge_keys = ["rel","features","startLemmas","relLemmas","endLemmas","start","end","score","weight","context","text","surfaceText","nodes","uri","sources"]

'''

I went home.

We were eating hamburgers.

He kicked the ball.

The food was delicious.


'''

def similarity_check(opener,thing_one,thing_two):
    request = _base + "assoc/c/%s/%s?filter=/c/%s/%s&limit=1" % (_lang,thing_one,_lang,thing_two)
    page = opener.open(request)
    return json.load(page)

def associated_with(opener,concept):
    request = _base + "assoc/list/%s/%s" % (_lang,concept)
    page = opener.open(request)
    return json.load(page)

def concept_info(opener,concept):
    request = _base + "c/%s/%s?filter=/c/en"% (_lang,concept)
    page = opener.open(request)
    return json.load(page)


def sub_powerset(sentence_list):
    ''' Takes a sentence as a list, and returns a sub-powerset:
    if the sentence is: ['i', 'ate', 'a', 'delicious', 'dinner']
    then this function will return:
    {'1': ['i', 'ate', 'a', 'delicious', 'dinner']
    '3': ['i ate a', 'ate a delicious', 'a delicious dinner']
    '2': ['i ate', 'ate a', 'a delicious', 'delicious dinner']
    '5': ['i ate a delicious dinner']
    '4': ['i ate a delicious', 'ate a delicious dinner']}
    '''
    sub_powerset = {} 
    len_list = len(sentence_list)
    len_list_p = len_list +1
    num_lists = (len_list*(len_list_p))/2 # we will return [m(m+1)]/2 lists, where 'm' is the number of words in the sentence.
    start = 0
    for offset in range(1,len_list_p):
        start = 0
        stop_at = len_list_p - offset
        inner_list = []
        for i in range(0,stop_at):
            inner_list.append(" ".join(sentence_list[start:start+offset]))
            start += 1
        sub_powerset[str(offset)] = inner_list
    print str(sub_powerset).replace("],","]\n")
    return sub_powerset
    

try: 
    opener = urllib2.build_opener(urllib2.HTTPHandler)


    
    #result1 = similarity_check(opener,thing_one,thing_two)
    #result2 = associated_with(opener,concept)
    sentence = "I ate a delicious dinner."
    sentence = sentence.strip(".?!")
    sentence = sentence.lower()
    print sentence
    sentence_list = sentence.split(" ")
    print sentence_list
    combinations = sub_powerset(sentence_list)
    print combinations["1"][0]
    result3 = concept_info(opener,"eat")#combinations["1"][0])
    result = result3
    print result
    try:
        edges = result["edges"]
        for edge in edges:
            try:
                print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
                for key in edge.keys():
                    print "key: "+key
                    print edge[key]
                print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            except KeyError:
                print "Key: '"+key+"' is not present."
    except KeyError:
        print "No edges returned."

except urllib2.HTTPError:
    raise

class node:
    
    def __init__(self,node_type):
        self.node_type = node_type


