'''
Created on Mar 9, 2013

@author: Andrew W.E. McDonald
'''
import middleman
import admin
import re
import gauntlet

class conductor:
    
    def __init__(self):
        self.log = admin.init_logger("conductor", admin.LOG_MODE)
        self.lang_proc = middleman.LanguageProcessor()
        
    def get_dict_entry(self, dict, entry):
        try:
            return dict[entry]
        except ValueError:
            self.log.error("Key '%s' was not present in dictionary returned by Stanford CoreNLP! This will almost certainly lead to subpar results (if any at all)", entry)
        return None
    
    def get_alternate_concepts(self,sentence):
        parse_results, parse_tree = self.lang_proc.parse(sentence) # returns a list of lists. each list contains one word from the sentence in index '0', and a dictionary 
        # containing the following information (the keys are listed): 'NamedEntityTag', 'CharacterOffsetEnd', 'CharacterOffsetBegin', 'PartOfSpeech', and 'Lemma'
        lemmas_with_pos = {} # this will be a dictionary such that the key is the lemma, and the value is the part of speech 
        lemma_list = [] # need a separate list of the lemmas so that when we build the sub-powerset, the order of the words isn't changed (as it might be with a dictionary) 
        for element in parse_results:
            word = element[0]
            if re.match(".*[.?!,;:'\"/-].*", word):
                continue # ConceptNet either seems to ignore punctuation or produce odd results. Either way, we probably don't want to leave the punctuation there for the moment.
            the_dict = element[1]
            self.log.info("word: %s -- %s",word,str(the_dict))
            current_lemma = self.get_dict_entry(the_dict,"Lemma")
            lemmas_with_pos[current_lemma] = self.get_dict_entry(the_dict,"PartOfSpeech")
            lemma_list.append(current_lemma)
        subpowerset = self.lang_proc.sub_powerset(lemma_list)
        num_lists = len(subpowerset) + 1
        concept_net_query_result_dictionary = {}
        for i in range(1,num_lists): # query concept net for all elements of all lists
            # just update the dictionary, so we end up with a dictionary such that:: key: concept => value: cnet results. So, for every entry of 'subpowerset',
            # we will get an entry in 'concept_net_query_result_dictionary' (though the value may be 'None' if ConceptNet didn't have anything to return.
            concept_net_query_result_dictionary.update(self.lang_proc.query_concept_net(subpowerset[str(i)]))
        cnqrd_keys = concept_net_query_result_dictionary.keys()
        self.log.debug("keys: %s",str(cnqrd_keys))
        for key in cnqrd_keys:
            self.log.debug("key: %s -- %s",key,str(concept_net_query_result_dictionary[key]))
        return lemma_list, lemmas_with_pos, concept_net_query_result_dictionary
    
    def get_similarities_between_original_and_replacements(self, filtered_cnet_result_dictionary):
        ''' Goes through the filtered results and checks the similarity between each potential replacement and the 'key' (either the lemmatized version of a word from the initial sentence,
        or a group of the lemmatized versions of the words from the initial sentence.)
        
        Once finished, a dictionary will be returned with the same keys as the input dictionary, but the values will be a list of lists. Each inner list will be of the form: [replacement, potential].
        potential will be calculated like so: potential = validity * similarity
        
        Finally, each list of lists will be sorted in reverse order with respect to each inner list's potential (so, index '0' will contain the inner list with the greatest potential).
        
        '''
        key_set = filtered_cnet_result_dictionary.keys()
        post_similarity_check_dict = {} 
        for key in key_set:
            these_replacements = filtered_cnet_result_dictionary[key]
            list_of_potential_replacements = []
            for possible_replacement in these_replacements:
                result = self.lang_proc.do_similarity_check(key, possible_replacement["start"][0], False) 
                if result[0] == "":
                    continue
                similarity = result[1] # is already a float
                potential = similarity * possible_replacement["validity"]
                list_of_potential_replacements.append([result[0],potential])
            list_of_potential_replacements.sort(key=lambda x: -x[1]) # sort in reverse order
            post_similarity_check_dict[key] = list_of_potential_replacements 
        for key in key_set:
            self.log.debug("key: %s -- %s",key,str(post_similarity_check_dict[key]))
        return post_similarity_check_dict
    