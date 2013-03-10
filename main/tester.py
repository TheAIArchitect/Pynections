'''
Created on Mar 7, 2013

@author: Andrew W.E. McDonald


This tests various things,
'''
import admin
import conductor
import gauntlet

the_conductor = conductor.conductor()
sent = "I am a funny person."
lemmas_with_pos, cnet_query_result_dict = the_conductor.get_alternate_concepts(sent.lower()) # must give lowercase sentence.
the_gauntlet = gauntlet.gauntlet()
parsed_cnet_result_dict = the_gauntlet.parse_cnet_result_dictionary(cnet_query_result_dict)
filtered_results = the_gauntlet.trim_useless_results(parsed_cnet_result_dict,lemmas_with_pos)
the_conductor.get_similarities_between_original_and_replacements(filtered_results)

# NEXT: Decide if we're going to switch the replacments when we do the similarity check (maybe just don't.. that's my inclination now). Then,
# we need to just string together the new sentences based upon the lists returned! (and, see note below). 

# We also have to use something like "if a in b" to see if a substitution has part of another word in it (so, take the lemmatized keys in the dict returned by the_gauntlet, 
# and if a replacement comes from one of the lists of the keys that contain another key, we don't look at anything from the other key.).
    