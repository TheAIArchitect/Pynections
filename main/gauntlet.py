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
        if result == None:
            self.log.warning("No match found in 'concept_extractor' for concept: %s",to_extract)
            return ["","",""]
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
    
    def pos_matcher(self, cnet_pos, corenlp_pos):
        ''' Matches ConceptNet part of speech tags with Stanford CoreNLP part of speech tags (where applicable)
        As a side note, ConceptNet uses WordNet's system (displayed below), while CoreNLP uses the Penn Treebank system.
        WordNet's system may be found at: 
        Penn Treebank's system may be found at: http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html 
        
        If a '1' is returned, cnet_pos and corenlp_pos are of the same general type
        If a '0' is returned, it is unknown whether cnet_pos and corenlp_pos are of the same type
        if a '-1' is returned, cnet_pos and corenlp_pose are NOT of the same type
        '''
        if cnet_pos == "" or corenlp_pos == "":
            return 0
        cnet_noun = 'n'
        cnet_verb = 'v'
        cnet_adj = 'a'
        cnet_adj_satellite = 's' # what is this??
        cnet_adverb = 'r' 
        corenlp_adj = ["JJ","JJR","JJS"]
        corenlp_noun = ["NN","NNS","NNP","NNPS"]
        corenlp_verb = ["VB","VBD","VBG","VBN","VBP","VBZ"]
        corenlp_adverb = ["RB", "RBR", "RBS"]
        #corenlp_adj_satellite #????
        if cnet_pos == cnet_noun:
            if corenlp_pos in corenlp_noun:
                return 1
        elif cnet_pos == cnet_verb:
            if corenlp_pos in corenlp_verb:
                return 1
        elif cnet_pos == cnet_adj:
            if corenlp_pos in corenlp_adj:
                return 1
        elif cnet_pos == cnet_adj_satellite:
            return 0
        elif cnet_pos == cnet_adverb:
            if corenlp_pos in corenlp_adverb:
                return 1
        return -1
             
    
    def trim_useless_results(self, parsed_cnet_result_dict, lemmas_with_PoS):
        ''' removes results with the following relations: "HasContext", "Causes", "AtLocation", "DesireOf", "DerivedFrom", any others??
        removes results that are identical to the concept that searched for them.
        Also removes results that are of the wrong part of speech (if part of speech is available for both concepts
        '''
        relations_to_remove = ["HasContext","Causes","AtLocation","DesireOf", "DerivedFrom"] 
        key_set = parsed_cnet_result_dict.keys()
        lemmas_keys = lemmas_with_PoS.keys()
        filtered_cnet_result_dict = {}
        for key in key_set:
            this_concepts_edges = parsed_cnet_result_dict[key]
            filtered_edge_list = []
            if key in lemmas_keys: # we don't want to try to get the part of speech for a combination of more than 1 lemma, for example, "I went". There won't be a part of speech for that. 
                this_PoS = lemmas_with_PoS[key].lower()
            else:
                this_PoS = ""
            for this_edge in this_concepts_edges:
                rel = this_edge["rel"]
                if rel in relations_to_remove:  # search through the list of relations to remove
                    continue
                start = this_edge["start"]
                if key.__eq__(start[0]): # start[0] has the first part of the concept returned. If this matches the key, it's useless to us.
                    continue
                pos_test_result = self.pos_matcher(start[1], this_PoS) # make sure that both concepts have the same part of speech, if available
                if pos_test_result < 0:
                    continue
                # if we've made it to this point, then the edge in question has survived this round
                filtered_edge_list.append(this_edge)
            filtered_cnet_result_dict[key] = filtered_edge_list
        new_key_set = filtered_cnet_result_dict.keys()
        self.log.debug("keys: %s",str(new_key_set))
        for key in new_key_set:
            self.log.debug("key: %s -- %s",key,str(filtered_cnet_result_dict[key]))
        return filtered_cnet_result_dict
            
            
    def select_alternate_concepts(self,lemma_list,conceptnet_lookup_results_dictionary):
        ''' This function takes a list of the lemmas of the sentence to be paraphrased (one per word), and the results from querying ConceptNet.
        The results from ConceptNet for each concept (each word, each pair of words, each set of 3 words, etc.) will be looked at: the more results a
        given concept has, the more likely we are to use it. An example would be if in a sentence, word 1 has 10 alternate concepts, and word two has 5 alternate concepts, 
        but words 1 and 2 (as a single concept) have 20 alternate concepts, then we put "1 and 2" as a more important alternative than the alternates for just 1 and just 2. 
        '''
        # go through each key in the dictionary and see how many alternatives each one has (maybe do some Q.C. first/during)
        # eliminate conflicts: if we want to use an alt. concept for "eat dinner", we must make sure that we don't also include an alt. for "dinner" alone.
        # order the results?
        
    def construct_new_sentences(self, cleaned_crunched_key_lists, post_similarity_check_dict):
        ''' Goes through 'cleaned_crunched_key_list', and creates new sentences using the words (values) returned from using the keys from the crunched 
        key list, and orders the sentences by summing the 'potential' values of all of the included words.
        '''
        all_sents = []
        for key_list in cleaned_crunched_key_lists:
            words_to_use = []
            for key in key_list:
                values = post_similarity_check_dict[key]
                if values == []:
                    values = [key, 0] # if for some reason, there aren't any alternatives (shoudn't be the case if the key/value pair has made it this far), then we just use the key, and set the potential to '0'.
                words_to_use.append(values)
            all_sents.append(words_to_use)
        # now we have a list (all_sents), of lists (words_to_use), of lists (values), of 'word, potential' pairs.
        for sent in all_sents:
            self.log.debug("sent: %s",str(sent))
            # call an altered version of the recursive cruncher (call it recursive word cruncher)
        
    def recursive_key_cruncher(self,crunched, to_crunch):
        ''' recursivley creates a 'sub-powerset' of to_crunch. 
        
        Example: 
        
        if "to_crunch" is this: [[['the'], ['the', 'boy'], ['the', 'boy', 'went']], [['boy'], ['boy', 'went']], [['went'], ['went', 'home']], [['home']]]
        
        then the result will be:
        
        [[['home'], ['went'], ['boy'], ['the']]
         [['home'], ['went', 'home'], ['boy'], ['the']]
         [['home'], ['went'], ['boy', 'went'], ['the']]
         [['home'], ['went', 'home'], ['boy', 'went'], ['the']]
         [['home'], ['went'], ['boy'], ['the', 'boy']]
         [['home'], ['went', 'home'], ['boy'], ['the', 'boy']]
         [['home'], ['went'], ['boy', 'went'], ['the', 'boy']]
         [['home'], ['went', 'home'], ['boy', 'went'], ['the', 'boy']]
         [['home'], ['went'], ['boy'], ['the', 'boy', 'went']]
         [['home'], ['went', 'home'], ['boy'], ['the', 'boy', 'went']]
         [['home'], ['went'], ['boy', 'went'], ['the', 'boy', 'went']]
         [['home'], ['went', 'home'], ['boy', 'went'], ['the', 'boy', 'went']]]
         
         the function, "clean up crunched keys" makes this more useful (see function for an example of it's output) by doing things like reversing the lists, 
         removing duplicates, etc.
        '''
        if len(to_crunch) <= 1:
            for key_list in to_crunch[0]:
                crunched.append([key_list]) 
            return crunched
        elif crunched == []:
            print "calling self:: to crunch is: ", str(to_crunch)
            crunched = self.recursive_key_cruncher(crunched,to_crunch[1:])
            print "returned. crunched is: ", str(crunched), " and to crunch is: ",str(to_crunch)
        new_crunched = []
        for key_list in to_crunch[0]:
            print "key list in to_crunch: ", key_list
            for other_key_list in crunched:
                print other_key_list
                concatted = other_key_list + [key_list]
                print "concatted: "+str(concatted)
                new_crunched.append(concatted) 
        print "new_crunched is: \n"+str(new_crunched).replace("]],","]]\n")
        return new_crunched

    def clean_up_crunched_keys(self, lemma_list, crunched_keys):
        ''' removes duplicate keys from the crunched_keys, and joins the inner key lists (so, a two word key that was split to look like ['the', 'boy'] will be joined to look like "the boy'.
        
        an example of the input can be found in "recusive_key_cruncher". The output from this function, assuming that input, will be:
        
        ['the', 'boy', 'went', 'home']
        ['the', 'boy', 'went home']
        ['the', 'boy went', 'home']
        ['the boy', 'went', 'home']
        ['the boy', 'went home']
        ['the boy went', 'home']
        
        ''' 
        cleaned_key_list_list = []
        for key_list in crunched_keys:
            key_list.reverse() # the cruncher ('recursive_key_cruncher') produced reversed lists. Now, we reverse the reversal.  
            cleaned_key_list = []
            used_lemmas = []
            for key_as_list in key_list:
                skip_this_key = False
                for key_token in key_as_list:
                    used_lemma = lemma_list.index(key_token)
                    if used_lemma in used_lemmas:
                        skip_this_key = True
                        break
                    used_lemmas.append(used_lemma)
                if not skip_this_key:
                    cleaned_key_list.append(' '.join(key_as_list))
            cleaned_key_list_list.append(cleaned_key_list) 
        no_duplicates = []
        for inner_list in cleaned_key_list_list:
            if inner_list in no_duplicates:
                continue
            no_duplicates.append(inner_list) 
        return no_duplicates
        
        
    def get_key_lists_for_new_sents(self, lemma_list, post_similarity_check_dict):
        ''' go through and create lists of keys that represent the possible sentence formations, making sure to not include a concept twice.
        For example, if the keys are ["i","go","to","the","mall","go to","the mall"], then one possible key list would be ["i","go","to","the","mall"], and another
        would be, ["i","go to","the mall"]. We would want to eliminate the possibility of, ["i","go","go to","the","the mall"].
        
        These key lists will (in create_alternate_sentences), be used to get the values from the dictionary entries of the appropriate keys in each key list (in order).
        '''
        key_set = post_similarity_check_dict.keys()
        keys_by_size = {}
        num_words_in_sentence = len(lemma_list)
        max_key_length = 0 # in terms of number of words in the key
        for key in key_set:
            split_key = key.split()
            num_words = len(split_key)
            if num_words > max_key_length:
                max_key_length = num_words
            if num_words in keys_by_size.keys():
                keys_by_size[num_words].append(split_key)
            else:
                keys_by_size[num_words] = [split_key]
        # now go through and find all keys containing the first lemma, then second lemma, etc.
        ordered_key_lists = []
        for i in range(0,num_words_in_sentence):
            current_lemma = lemma_list[i]
            keys_with_current_lemma = []
            for j in range(1, max_key_length+1):
                current_keys = keys_by_size[j]
                for key in current_keys:
                    if current_lemma in key:
                        keys_with_current_lemma.append(key)
            ordered_key_lists.append(keys_with_current_lemma) 
        self.log.debug("ordered key lists: %s",str(ordered_key_lists))
        crunched_keys = self.recursive_key_cruncher( [], ordered_key_lists)
        cleaned_crunched_keys = self.clean_up_crunched_keys( lemma_list, crunched_keys)
        return cleaned_crunched_keys
        
            
    
    
        