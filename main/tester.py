'''
Created on Mar 7, 2013

@author: Andrew W.E. McDonald


This tests various things,
'''

import admin
import conductor
import gauntlet

the_conductor = conductor.conductor()
sent = "The boy went home."#to the field and kicked the ball."
lemma_list, lemmas_with_pos, cnet_query_result_dict = the_conductor.get_alternate_concepts(sent.lower()) # must give lowercase sentence.
the_gauntlet = gauntlet.gauntlet()
parsed_cnet_result_dict = the_gauntlet.parse_cnet_result_dictionary(cnet_query_result_dict)
filtered_results = the_gauntlet.trim_useless_results(parsed_cnet_result_dict,lemmas_with_pos)
post_similarity_check_dict = the_conductor.get_similarities_between_original_and_replacements(filtered_results)
cleaned_crunched_key_lists = the_gauntlet.get_key_lists_for_new_sents(lemma_list, post_similarity_check_dict)
the_gauntlet.construct_new_sentences(cleaned_crunched_key_lists, post_similarity_check_dict)


# NEXT: Need to just string together the new sentences based upon the lists returned! (and, see note below). 

# We also have to use something like "if a in b" to see if a substitution has part of another word in it (so, take the lemmatized keys in the dict returned by the_gauntlet, 
# and if a replacement comes from one of the lists of the keys that contain another key, we don't look at anything from the other key.).
''' 
def recursive_word_cruncher(self,crunched, to_crunch):
         recursivley creates a 'sub-powerset' of to_crunch. 
        
        Example: 
        
        if "to_crunch" is this: [[['the'], ['the', 'boy'], ['the', 'boy', 'went']], [['boy'], ['boy', 'went']], [['went'], ['went', 'home']], [['home']]]
       
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
'''