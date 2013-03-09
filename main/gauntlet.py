'''
Created on Mar 9, 2013

@author: Andrew W.E. McDonald
'''
import admin

class gauntlet:
    
    def __init__(self):
        self.log = admin.init_logger("gauntlet", admin.LOG_MODE)
        
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
    
    
        