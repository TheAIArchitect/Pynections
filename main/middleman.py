'''
Created on Mar 4, 2013

@author: Andrew W.E. McDonald

middleman is the "middleman" between corenlp_iface and cnet_iface.
'''
import corenlp_iface
import cnet_iface
from pprint import pprint

class LanguageProcessor:
    
    def __init__(self):
        self.corenlp = corenlp_iface.StanfordNLP()
        
        
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
        # The keys of the resulting dictionary are: 'NamedEntityTag', 'CharacterOffsetEnd', 'CharacterOffsetBegin', 'PartOfSpeech', and 'Lemma'
        # 'NamedEntityTag' is 
        # 'CharacterOffestEnd' is 
        # 'CharacterOffsetBegin' is
        # 'PartOfSpeech' is the part of speech of the word in the sentence
        # 'Lemma' is the lemmatized version of the word. This is very important for us, because this is the version of the word that we will use when querying ConceptNet
        # The lemma may be retrieved like so: parsed["sentences"][0]["words"][0][1]["Lemma"]
        
        ''' get the named entity tag, part of speech, and lemma for each word. Then we can query concept net, and disregard results that aren't of the same POS. 
        '''
        