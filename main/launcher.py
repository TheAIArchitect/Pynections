'''
Created on Mar 11, 2013

@author: Andrew W.E. McDonald
'''
import conductor, gauntlet, admin
import time

class launcher:
    
    def __init__(self):
        self.log = admin.init_logger("launcher", admin.LOG_MODE)
        self.the_conductor = conductor.conductor()
        self.the_gauntlet = gauntlet.gauntlet()
        
    def run(self,sent):
        lemma_list, lemmas_with_pos, cnet_query_result_dict = self.the_conductor.get_alternate_concepts(sent.lower()) # must give lowercase sentence.
        parsed_cnet_result_dict = self.the_gauntlet.parse_cnet_result_dictionary(cnet_query_result_dict)
        self.log.info("parsed_cnet_result_dict: %s",str(parsed_cnet_result_dict))
        filtered_results = self.the_gauntlet.trim_useless_results(parsed_cnet_result_dict,lemmas_with_pos)
        self.log.info("filtered_results: %s",str(filtered_results))
        post_similarity_check_dict = self.the_conductor.get_similarities_between_original_and_replacements(filtered_results)
        self.log.info("post_similarity_check_dict: %s",str(post_similarity_check_dict))
        cleaned_crunched_key_lists = self.the_gauntlet.get_key_lists_for_new_sents(lemma_list, post_similarity_check_dict)
        new_sents_with_potential = self.the_gauntlet.construct_new_sentences(cleaned_crunched_key_lists, post_similarity_check_dict)    
        return new_sents_with_potential
    
    

if __name__ == "__main__":
    
    s1 = "The boy went to the field and kicked the soccer ball."
    s2 = "He returned to his house in the evening."
    s3 = "My computer is trying to construct english sentences."
    s4 = "Poor planning leads to missed deadlines."
    s5 = "Running is a form of exercise."
    s6 = "The man ate a bagel this morning."
    s7 = "James likes to drink and play pool."
    s8 = "Coming up with test sentences is not easy."
    s9 = "I have a little dog."
    s10 = "I hope my train is on time today."
    s11 = "Testing these sentences will take a long time."
    s12 = "I do not have high hopes for some of these sentences."
    s13 = "Big and sturdy wooden desks are nice to work on, and to prop your feet on."
    s14 = "The parking ticket my girlfriend got cost her 30 dollars."
    s15 = "Parking tickets make people very unhappy."
    original_sents = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15]
    file_names = ["s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","s12","s13","s14","s15"]
    time_taken = 0
    num_original_sents = len(original_sents)
    the_launcher  =  launcher()
    
    for sent_number in range(14,num_original_sents):
        start_time = time.time()
        new_sents = the_launcher.run(original_sents[sent_number])
        end_time = time.time()
        elapsed = end_time - start_time
        time_taken += elapsed
        #time_taken.append(elapsed)
        
        time.sleep(2) # just to let the logger get everything out before we start 'print'ing
        path = "../results/"
        the_file = open(path+file_names[sent_number]+".txt",'w')
        line_1 = "Alternative sentences for input sentence: \n'"+original_sents[sent_number]+"' -- elapsed time: "+str(elapsed)+" seconds."
        the_file.write(line_1+"\n")
        print line_1
        line_2 = "---------------------------------------------------------------------------------------"
        the_file.write(line_2+"\n")
        print line_2
        number = 0
        next_line = ""
        for sent in new_sents:
            number += 1 
            next_line = str(number)+": "+sent 
            the_file.write(next_line+"\n")
            print next_line
        the_file.close()
        #exit()
    #total_time = sum(time_taken)
    #num_times = len(time_taken)
    #avg_time = time_taken/float(len(original_sents)) 
    #print "average time per sentence: "+str(avg_time)+" seconds."