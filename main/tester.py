'''
Created on Mar 7, 2013

@author: Andrew W.E. McDonald


This tests various things,
'''
import admin
import conductor
import middleman
import gauntlet

my_conductor = conductor.conductor()
lemmas_with_pos, cnet_query_result_dict = my_conductor.get_alternate_concepts("I ate good food.")
the_gauntlet = gauntlet.gauntlet()
the_gauntlet.parse_cnet_result_dictionary(cnet_query_result_dict)

## NEXT: we go through each key in the dictionary returned by the_gauntlet, and we remove relations that are "relatedTo" (especially if the word is a noun). 
# Then we keep trimming down the list of possible substitutions, and once we have a list that may be decent, we check the similarity of those using ConceptNet,
# and then order the substitutions. 

# We also have to use something like "if a in b" to see if a substitution has part of another word in it (so, take the lemmatized keys in the dict returned by the_gauntlet, 
# and if a replacement comes from one of the lists of the keys that contain another key, we don't look at anything from the other key.).
    