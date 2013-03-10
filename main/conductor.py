'''
Created on Mar 9, 2013

@author: Andrew W.E. McDonald
'''
import middleman
import admin
import re

class conductor:
    
    def __init__(self):
        self.log = admin.init_logger("conductor", admin.LOG_MODE)
        
    def get_dict_entry(self, dict, entry):
        try:
            return dict[entry]
        except ValueError:
            self.log.error("Key '%s' was not present in dictionary returned by Stanford CoreNLP! This will almost certainly lead to subpar results (if any at all)", entry)
        return None
    
    def get_alternate_concepts(self,sentence):
        lang_proc = middleman.LanguageProcessor()
        parse_results, parse_tree = lang_proc.parse(sentence) # returns a list of lists. each list contains one word from the sentence in index '0', and a dictionary 
        # containing the following information (the keys are listed): 'NamedEntityTag', 'CharacterOffsetEnd', 'CharacterOffsetBegin', 'PartOfSpeech', and 'Lemma'
        lemmas_with_pos = {} # this will be a dictionary such that the key is the lemma, and the value is the part of speech 
        for element in parse_results:
            word = element[0]
            if re.match(".*[.?!,;:'\"/-].*", word):
                continue # ConceptNet either seems to ignore punctuation or produce odd results. Either way, we probably don't want to leave the punctuation there for the moment.
            the_dict = element[1]
            self.log.info("word: %s -- %s",word,str(the_dict))
            lemmas_with_pos[self.get_dict_entry(the_dict,"Lemma")] = self.get_dict_entry(the_dict,"PartOfSpeech")
        subpowerset = lang_proc.sub_powerset(lemmas_with_pos.keys())
        num_lists = len(subpowerset) + 1
        concept_net_query_result_dictionary = {}
        for i in range(1,num_lists): # query concept net for all elements of all lists
            # just update the dictionary, so we end up with a dictionary such that:: key: concept => value: cnet results. So, for every entry of 'subpowerset',
            # we will get an entry in 'concept_net_query_result_dictionary' (though the value may be 'None' if ConceptNet didn't have anything to return.
            concept_net_query_result_dictionary.update(lang_proc.query_concept_net(subpowerset[str(i)]))
        cnqrd_keys = concept_net_query_result_dictionary.keys()
        self.log.debug("keys: %s",str(cnqrd_keys))
        for key in cnqrd_keys:
            self.log.debug("key: %s -- %s",key,str(concept_net_query_result_dictionary[key]))
        return lemmas_with_pos, concept_net_query_result_dictionary
    