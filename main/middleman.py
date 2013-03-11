'''
Created on Mar 4, 2013

@author: Andrew W.E. McDonald

middleman is the "middleman" between corenlp_iface and cnet_iface.
'''
import corenlp_iface
import cnet_iface
import admin
from pprint import pprint


class LanguageProcessor:
    
    def __init__(self, skip_corenlp_init = False):
        ''' if 'skip_corenlp_init' is 'True', there will be no corenlp functionality, however, the class will load much much faster.
        so, good to use when testing things that don't depend upon corenlp. 
        '''
        if not skip_corenlp_init:
            self.corenlp = corenlp_iface.StanfordNLP()
        self.cnet = cnet_iface.cnet_iface() 
        self.log = admin.init_logger("middleman", admin.LOG_MODE)
        
    def parse(self,text):
        parsed = self.corenlp.parse(text)
        # pprint(parsed)
        # parsed is a dictionary, one of it's keys is 'sentences'. 'sentences' is a list, one item per input sentence. each item is a dictionary.
        # each of these dictionaries contains the following keys: 'parsetree', 'text', 'dependencies', 'words'
        # 'parsetree' contains an inline parse tree of the sentence (accessed by: parsed["sentences"][0]["parsetree"] -- assuming you are after sentence '0')
        # 'text' is the original text of the sentence that was parsed
        # 'dependencies' is a list of lists, each inner list revealing a grammatical dependency within the sentence
        # 'words' is a list of lists. each inner list is of the form ["word", "dictionary of information about this word"], where 'word' is the word in question.
        # An example of getting the dictionary for the first word in the first sentence of parsed text is: parsed["sentences"][0]["words"][0][1]
        # The keys of the resulting dictionary are: 
        # 'NamedEntityTag' is 
        # 'CharacterOffestEnd' is 
        # 'CharacterOffsetBegin' is
        # 'PartOfSpeech' is the part of speech of the word in the sentence
        # 'Lemma' is the lemmatized version of the word. This is very important for us, because this is the version of the word that we will use when querying ConceptNet
        # The lemma may be retrieved like so: parsed["sentences"][0]["words"][0][1]["Lemma"]
        
        #word_info_we_want = [] #list of dictionaries... one per word
        word_info_we_want = parsed["sentences"][0]["words"] # this was in a loop (see line below) because I thought we might only want some of the information, but it seems like more work to pick out the two things we don't need
        #for word_info in parsed["sentences"][0]["words"]:
        #    word_info_we_want.append(word_info)
        return word_info_we_want, parsed["sentences"][0]["parsetree"] 
        '''Then we can query concept net, and disregard results that aren't of the same POS. 
        '''
    
    def query_concept_net(self,concept_list):
            ''' Takes a list of lemmatized concepts (though not necessarily single word concepts)
            
            returns ....
            '''
            # From "get_concept_info": Interested in "score", "weight", "context", "rel"
            # From "associated_with": interested in 'similar' (this is a list of lists, each list has a concept and a number that is supposed to suggest the closeness of the association)
            # From "similarity_check": Interested in 'similar'. This is the same 
            cnet_results = {}
            for concept in concept_list:
                #cnet_results[lemma] = cnet.concept_info(concept)
                self.log.info("lemma: %s",concept)
                cnet_results[concept] = self.cnet.concept_info(concept,admin.NUM_EDGES_TO_RETURN,admin.EDGE_KEYS_IN_USE)
                self.log.debug("ConceptNet Info for concept '%s' is:\n%s",concept,str(cnet_results[concept]))
                #self.log.info("--=[ %s ]=--\n%s",lemma)
            return cnet_results # format:: key: concept => value: result of calling cnet.concept_info .. which is a list of the retured edges, each element  being a dictionary of information (JSON format)
                
         
    def sub_powerset(self,sentence_list):
        ''' Takes a sentence as a list, and returns a sub-powerset:
        if the sentence is: ['i', 'ate', 'a', 'delicious', 'dinner']
        then this function will return:
        {'1': ['i', 'ate', 'a', 'delicious', 'dinner']
        '3': ['i ate a', 'ate a delicious', 'a delicious dinner']
        '2': ['i ate', 'ate a', 'a delicious', 'delicious dinner']
        '5': ['i ate a delicious dinner']
        '4': ['i ate a delicious', 'ate a delicious dinner']}
        
        NOTE: for sake of 'intuitiveness' lists that have '1' token per element are in dictionary '1',
        lists that have '2' tokens per element are in dictionary '2', etc.. So, there is no '0' key.
        
        '''
        sub_powerset = {} 
        len_list = len(sentence_list)
        len_list_p = len_list +1
        start = 0
        for offset in range(1,len_list_p):
            start = 0
            stop_at = len_list_p - offset
            inner_list = []
            for i in range(0,stop_at):
                inner_list.append(" ".join(sentence_list[start:start+offset]))
                start += 1
            sub_powerset[str(offset)] = inner_list
        self.log.debug(str(sub_powerset))#.replace("],","]\n")
        return sub_powerset
        
    def do_similarity_check(self, original, replacement, should_swap_replacement_for_new_replacement = True):
        ''' checks the similarity between 'original' and 'replacement'. Returns a list, [new_replacement, similarity], 
        where 'new_replacement' is the concept returned by the similarity check.
        
        "should_swap_replacement_for_new_replacement" will return the concept returned by the similarity check as 'new_replacement', if True.
        If false, it will return 'replacement' as 'new_replacement'. Note that if 'True', 'new_replacement' will have to be parsed -- as it will be in the form of
        "/c/en/<actual concept>/<possible pos>/<possible disambiguation>". This can be done via 'gauntlet's 'concept_extractor'.
        '''
        result = self.cnet.similarity_check(original,replacement, 1) # we only want the best result
        if len(result) > 0:
            new_concept = result[0][0]
            try:
                new_concept_similarity = float(result[0][1])
                #self.log.debug("new concept: %s, similarity: %s", new_concept, result[0][1])
            except ValueError:
                self.log.error("Could not convert similarity to float. This is an issue... similarity set to '0'. This will neutralize potential replacement '%s'.",result[0][1],replacement)
                new_concept_similarity = 0 
            if should_swap_replacement_for_new_replacement:
                return [new_concept, new_concept_similarity]
            else:
                return [replacement, new_concept_similarity]
        return ["",0] # what else to do?
        
        