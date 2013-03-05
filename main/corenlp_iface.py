#!/usr/bin/python
import simplejson as json
import pythoncorenlp.corenlp as corenlp
from pprint import pprint
import admin


log = admin.init_logger("corenlp_iface", admin.LOG_MODE)

class StanfordNLP:

    def __init__(self,stanford_corenlp_path="../lib/stanford-corenlp-2012-07-09/",properties_location="../lib/pythoncorenlp/"):
        try:
            self.stanford_parser = corenlp.StanfordCoreNLP(stanford_corenlp_path,properties_location)# This will take a little while to load.
        except:
            log.critical("StanfordCoreNLP could not load!")            
            raise

    def parse(self, text):
        return json.loads(self.stanford_parser.parse(text))

        
if __name__ == "__main__":
    nlp = StanfordNLP()
    result = nlp.parse("Hello world!  It is so beautiful.")
    pprint(result)

