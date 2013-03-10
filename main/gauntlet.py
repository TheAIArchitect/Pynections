'''
Created on Mar 9, 2013

@author: Andrew W.E. McDonald
'''
import admin
import re

class gauntlet:
    
    def __init__(self):
        self.log = admin.init_logger("gauntlet", admin.LOG_MODE)
        
    def concept_extractor(self,to_extract):
        result = re.match("(^/c/en/)([^/]+)(/*)([^/]*)(/*)([^/]*)",to_extract)
        # groups (assuming all matches):: 0-whole thing, 1-/c/en/, 2-concept, 3-'/', 4-part of speech, 5-'/', 6-disambiguation
        # groups (assuming only missing POS):: 0-whole thing, 1-/c/en/, 2-concept, 3-'/', 4-disambiguation, 5-'', 6-''
        # groups (assuming only missing disambiguation): 0-whole thing, 1-/c/en/, 2-concept, 3-'/', 4-part of speech, 5-'', 6-''
        # groups (assuming missing both POS and disambiguation): 0-whole thing, 1-/c/en/, 2-concept, 3-'', 4-'', 5-'', 6-''
        # NOTE: This is a bit of an issue, because if there is no POS and there is a disambiguation (or vice versa), its going to be hard to tell what group '4' is...
        # for the time being, we will just ignore both POS and disambiguation if either one is missing.
        if result.group(5) != "" and result.group(6) !=  "" and result.group(4) != "" and result.group(3) != "" : # then everything is present
            concept = result.group(2) 
            PoS = result.group(4)
            disambig = result.group(6)
        else:
            concept = result.group(2)
            PoS = ""
            disambig = ""
        return [concept, PoS, disambig]
        
    def parse_modified_edge_dictionary(self,modified_edge_dict):
        ''' Takes a dictionary looking like this:
        {'start': u'/c/en/food', 'score': 19.570192, 'end': u'/c/en/in_restaurant', 'weight': 4.0, 'rel': u'/r/AtLocation'}
        
        and returns a dictionary looking like this:
        
        {'start': u'food', 'validity': 78.280768, 'end': u'in_restaurant', 'rel': u'AtLocation'}
        '''
        key_set = modified_edge_dict.keys()
        # maybe check for an empty list first? e.g.: key: eat good -- []
        parsed_modified_edge_dict = {}
        weight_ok = False
        score_ok = False 
        for key in key_set:
            if key.__eq__("start"): # this is the potential substitution of the initial concept
                start = modified_edge_dict[key]
                parsed_modified_edge_dict[key] = self.concept_extractor(start)
            elif key.__eq__("end"): # this is hard to describe... basically, it's the second part of the concept. 
                end = modified_edge_dict[key]
                parsed_modified_edge_dict[key] = self.concept_extractor(end)
            elif key.__eq__("rel"): # this is the relationship between "start" and "end"
                rel = modified_edge_dict[key]
                parsed_modified_edge_dict[key] = rel[3:]
            elif key.__eq__("weight"): # this is the 'vaidity' of the relation
                weight = modified_edge_dict[key]
                weight_ok = True
            elif key.__eq__("score"): # I'm not totally sure what this is.. I think it has to do with the number of people that supported this concept
                score = modified_edge_dict[key]
                score_ok = True
        if score_ok and weight_ok:
            try:
                validity = float(weight)*float(score)
            except ValueError:
                self.log.error("Could not convert 'weight' (%s) or 'score' (%s) to floats!",weight,score)
                validity = 0 # Is there a better option? This makes it neurtral, which may not be good. 
        parsed_modified_edge_dict["validity"] = validity # this is a float, not a string.
        return parsed_modified_edge_dict
    
    def parse_cnet_result_dictionary(self, cnet_result_dict):
        ''' Takes the second output of conductor.get_alternate_concepts and strips away nonsense. 
        '''
        key_set = cnet_result_dict.keys()
        parsed_cnet_result_dict = {}
        for key in key_set:
            if cnet_result_dict[key] == []:
                continue # it's useless
            else:
                list_of_modified_edges = cnet_result_dict[key]
                parsed_modified_edges = []
                for modified_edge in list_of_modified_edges:
                    parsed_modified_edges.append(self.parse_modified_edge_dictionary(modified_edge))
                parsed_cnet_result_dict[key] = parsed_modified_edges 
        new_key_set = parsed_cnet_result_dict.keys()
        self.log.debug("keys: %s",str(new_key_set))
        for key in new_key_set:
            self.log.debug("key: %s -- %s",key,str(parsed_cnet_result_dict[key]))
        return parsed_cnet_result_dict 
                
    def order_potential_substitutions_by_similarity(self,initial,potential_replacements):
        ''' This queries ConceptNet via cnet_iface's 'similarity_check' function for each (initial,potential_replacement[i]) pair, where 'i' is the i'th central replacment, 
        and orders the potential replacements by the results of the queries. 
        '''
        pass
        
    def select_alternate_concepts(self,lemma_list,conceptnet_lookup_results_dictionary):
        ''' This function takes a list of the lemmas of the sentence to be paraphrased (one per word), and the results from querying ConceptNet.
        The results from ConceptNet for each concept (each word, each pair of words, each set of 3 words, etc.) will be looked at: the more results a
        given concept has, the more likely we are to use it. An example would be if in a sentence, word 1 has 10 alternate concepts, and word two has 5 alternate concepts, 
        but words 1 and 2 (as a single concept) have 20 alternate concepts, then we put "1 and 2" as a more important alternative than the alternates for just 1 and just 2. 
        '''
        
        # go through each key in the dictionary and see how many alternatives each one has (maybe do some Q.C. first/during)
        # eliminate conflicts: if we want to use an alt. concept for "eat dinner", we must make sure that we don't also include an alt. for "dinner" alone.
        # order the results?
        
        
    def create_alternate_sentences(self):
        pass
    
    
        