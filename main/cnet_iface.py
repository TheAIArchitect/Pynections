#!/usr/bin/python
'''
Created on Feb 19, 2013

@author: Andrew W.E. McDonald
'''
from __future__ import division
import urllib2
import simplejson as json
import admin

class cnet_ifact:

    _base = "http://conceptnet5.media.mit.edu/data/5.1/"
    _lang = "en"
    
    node_type = ["concept","frame","relation","assertion","sense"]
    edge_keys = ["rel","features","startLemmas","relLemmas","endLemmas","start","end","score","weight","context","text","surfaceText","nodes","uri","sources"]
    
    def __init__(self):  
        self.log = admin.init_logger("cnet_iface", admin.LOG_MODE)
        try: 
            self.opener = urllib2.build_opener(urllib2.HTTPHandler)
        except urllib2.HTTPError:
            self.log.critical("Error building opener")
    '''
    
    I went home.
    
    We were eating hamburgers.
    
    He kicked the ball.
    
    The food was delicious.
    
    
    '''
        
    def get_page(self,request):
        '''
        get request from ConceptNet
        '''
        try:
            page = self.opener.open(request)
            return json.load(page)
        except urllib2.HTTPError:
            self.log.critical("Error querying ConceptNet, could not connect!")
            raise # do I really want to raise an exception? Maybe we should try again a few times...
    
    def similarity_check(self,opener,thing_one,thing_two):
        '''
        Use ConceptNet's association request to see how similar two concepts are.
        '''
        request = self._base + "assoc/c/%s/%s?filter=/c/%s/%s&limit=1" % (self._lang,thing_one,self._lang,thing_two)
        answer = self.get_page(request)
        try:
            similar = answer["similar"]
            for elem in similar:
                self.log.info(elem)
            return similar
        except KeyError:
            self.log.warning("No similarities returned for concepts: '%s' and '%s'.",thing_one,thing_two)
            return None
    
    def associated_with(self,concept):
        '''
        Use ConceptNet to see what concepts are associated with other concepts. Also returns the 'degree' of association.
        '''
        request = self._base + "assoc/list/%s/%s" % (self._lang,concept)
        answer = self.get_page(request)
        try:
            similar = answer["similar"]
            for elem in similar:
                self.log.info(elem)
            return similar
        except KeyError:
            self.log.warning("No associations returned for concept: %s.",concept)
            return None
    
    def concept_info(self,concept):
        '''
        General query for ConceptNet. Returns information regarding the input concept.
        '''
        request = self._base + "c/%s/%s?filter=/c/en"% (self._lang,concept)
        answer = self.get_page(request)
        try:
            edges = answer["edges"]
            for edge in edges:
                try:
                    for key in edge.keys():
                        self.log.info("key: %s - %s",key,edge[key])
                except KeyError:
                    self.log.error("Key: '%s' is not present, but should be.",key)
        except KeyError:
            self.log.warning("No edges returned for concept: %s.", concept)
    
    
'''     
JUST FOR IDEAS:

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
'''
   
class node:
    
    def __init__(self,node_type):
        self.node_type = node_type


