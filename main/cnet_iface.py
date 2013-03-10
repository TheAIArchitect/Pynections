#!/usr/bin/python
'''
Created on Feb 19, 2013

@author: Andrew W.E. McDonald
'''
from __future__ import division
import urllib2
import simplejson as json
import admin
import re

class cnet_iface:

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
        try_again = True
        while try_again:
            try:
                page = self.opener.open(request)
                return json.load(page)
            except urllib2.HTTPError, urllib2.URLError:
                self.log.critical("Error querying ConceptNet, could not connect!")
                ans = raw_input("Try ConceptNet query again? (Y/n): ")
                if ans.lower()[0] == "n":
                    try_again = False
                    self.log.warning("Exiting...")
                    exit()
                
    
    def similarity_check(self, thing_one, thing_two, limit):
        '''
        Use ConceptNet's association request to see how similar two concepts are.
        '''
        request = self._base + "assoc/c/%s/%s?filter=/c/%s/%s&limit=%s" % (self._lang,thing_one,self._lang,thing_two,limit)
        answer = self.get_page(request)
        try:
            similar = answer["similar"]
            self.log.debug("similarity check between '%s' and '%s'",thing_one, thing_two)
            for elem in similar:
                self.log.debug(elem)
            return similar
        except KeyError:
            self.log.warning("No similarities returned for concepts: '%s' and '%s'.",thing_one, thing_two)
            return None
    
    def associated_with(self, concept, limit):
        '''
        Use ConceptNet to see what concepts are associated with other concepts. Also returns the 'degree' of association.
        '''
        request = self._base + "assoc/list/%s/%s&limit=%s" % (self._lang, concept,limit)
        answer = self.get_page(request)
        try:
            similar = answer["similar"]
            self.log.info("similarities for concept '%s':",concept)
            for elem in similar:
                self.log.info(elem)
            return similar
        except KeyError:
            self.log.warning("No associations returned for concept: %s.",concept)
            return None
        
    
    def concept_info(self,concept, limit, keys = None):
        '''
        General query for ConceptNet. Returns information regarding the input concept.
        
        Takes a concept (word, phrase), limit (max edges to return), keys (a list of the desired values to be returned. If omitted, the standard list of 'edges' dictionaries is returned)
        
        If 'keys' is not omitted, then a list is returned, with each item being a dictionary containing the desired keys from each original edge -- IF the entry is present in any given edge.
        When an entry is not present, the key is still included in the returned dictionary, but the corresponding value is "None".
        '''
        concept = concept.lower() # concepts MUST be in lowercase
        request = self._base + "c/%s/%s?filter=/c/en&limit=%s" % (self._lang, concept, limit)
        self.log.debug(request)
        answer = self.get_page(request)
        self.log.debug(answer)
        append = True 
        try:
            edges = answer["edges"]
            if keys != None: # If function was called with  special list of keys to get, then get them if they exist.
                edge_list = []
                for edge in edges:
                        edge_dict = {}
                        self.log.info("edge for concept '%s':",concept)
                        key_set = edge.keys()
                        for key in keys:
                            if key in key_set:
                                try:
                                    if key.__eq__("start") and re.match("/c/en/.*",edge[key]) == None:
                                        self.log.debug("not english: "+str(edge))
                                        append = False 
                                        break
                                    self.log.info("key: %s - %s",key,edge[key])
                                    edge_dict[key] = edge[key]
                                except KeyError:
                                    self.log.error("Key: '%s' is not present, but should be.",key)
                                    edge_dict[key] = None            
                            else:
                                edge_dict[key] = None
                        if append:
                            edge_list.append(edge_dict)
                        append = True 
            else: # if function was not called with special list of keys to get, then get all keys.
                edge_list = []
                for edge in edges:
                        edge_dict = {}
                        self.log.info("edge for concept '%s':",concept)
                        for key in edge.keys():
                            try:
                                #self.log.info("key: %s - %s",key,edge[key])
                                edge_dict[key] = edge[key]
                            except KeyError:
                                self.log.error("Key: '%s' is not present, but should be.",key)
                                edge_dict[key] = None
                        edge_list.append(edge_dict)   
        except KeyError:
            self.log.warning("No edges returned for concept: %s.", concept)
            edge_list = [] 
        self.log.info(edge_list)
        #print "edge_list is empty: "+str(edge_list == [])
        return edge_list
    
    
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


