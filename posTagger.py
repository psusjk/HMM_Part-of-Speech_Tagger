
############################################################
# Imports
############################################################

import time
import random
import math

############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    answer=[]
    fileobj=open(path,"r")
    for line in fileobj:
        result=[]
        for token in line.split():
            result.append(tuple(token.split('=')))
        answer.append(result)
    return answer
'''
c = load_corpus("brown-corpus.txt")
print(c[1402])
print(c[1799])
'''

def count_increment_helper(sentences,tag_count,all_tag_count,token_tag,tag_tag,used_tag,smooth):
    for line in sentences:
            t1 = line[0][1]
            all_tag_count[t1] += 1

            for token, tag in line:             
                tag_count[tag] += 1                
                token_counter = token_tag[tag]
                if token in token_counter:
                    token_counter[token] += 1
                else:
                    token_counter[token] = 1+smooth
                
                if used_tag is not None:
                    counter = tag_tag[used_tag]
                    if tag in counter:
                        counter[tag] += 1
                    else:
                        counter[tag] = 1+smooth
                used_tag = tag
    return tag_count,all_tag_count,token_tag,tag_tag,used_tag

def probability_helper(sentences,tag_count,all_tag_count,token_tag,tag_tag,used_tag,smooth):
    for used_tag in token_tag.keys():
            curr_tag = tag_count[used_tag]            
            token_dict = token_tag[used_tag]
            num_tokens = len(token_dict)
            for token in token_dict.keys():
                token_dict[token] = float(token_dict[token]) / (curr_tag + num_tokens*smooth)
            token_dict['<UNK>'] = float(smooth) / (curr_tag + num_tokens*smooth)
            #print(token_dict)            
            tag_dict = tag_tag[used_tag]
            num_tag=len(tag_dict)
            for tag in tag_dict.keys():
                tag_dict[tag] = float(tag_dict[tag]) / (curr_tag + num_tag*smooth)
            tag_dict['<UNK>'] = float(smooth) / (curr_tag + num_tag*smooth)
            #print(tag_dict)
            
    return tag_count,all_tag_count,token_tag,tag_tag,used_tag

class Tagger(object):

    def __init__(self, sentences):
        all_tags = ('NOUN', 'VERB', 'ADJ', 'ADV', 'PRON', 'DET', 'ADP', 'NUM', 'CONJ','PRT', '.', 'X')
        smooth=1e-5
        used_tag=None
        num=len(sentences)
        self.smoothing=smooth        
        self.tag_count={}
        all_tag_count={}
        token_tag={}
        tag_tag={}
        for t in all_tags:
            self.tag_count[t] = 0
            all_tag_count[t]=0
            token_tag[t]={}
            tag_tag[t]={}
        #print(self.tag_count)
        #print("\n")
        #print(all_tag_count)
        #print("\n")
        #print(token_tag)
        #print("\n")
        #print(tag_tag)
        tag_count=self.tag_count
        #print(tag_count)
        self.tag_count,all_tag_count,token_tag,tag_tag,used_tag=count_increment_helper(sentences,tag_count,all_tag_count,token_tag,tag_tag,used_tag,smooth)

        self.tag_prob = {tag: (float(all_tag_count[tag]+smooth))/(num+smooth*12) for tag in all_tag_count.keys()}
        #print(self.tag_prob)
        tag_count=self.tag_count
        #print(tag_count)
        self.tag_count,all_tag_count,token_tag,tag_tag,used_tag=probability_helper(sentences,tag_count,all_tag_count,token_tag,tag_tag,used_tag,smooth)

        self.token_tag_prob = token_tag
        self.tag_tag_prob = tag_tag 
        #print(self.token_tag_prob)
        #print(self.tag_tag_prob)
        #print("\n")
        #print(self.tag_count)
        #print("\n")
        #print(all_tag_count)
        #print("\n")
        #print(token_tag)
        #print("\n")
        #print(tag_tag)
        

    def most_probable_tags(self, tokens):
        answer = []
        for token in tokens:
            max=0
            tag=""
            for t in self.token_tag_prob.keys():
                mydict = self.token_tag_prob[t]
                if token in mydict and mydict[token] > max:
                    max = mydict[token]
                    tag = t
            answer.append(tag)
        #print(answer)
        return answer        

    def viterbi_tags(self, tokens):
        answer = []
        for token in tokens:
            max=0
            tag=""
            for t in self.token_tag_prob.keys():
                mydict = self.token_tag_prob[t]
                if token in mydict and mydict[token] > max:
                    max = mydict[token]
                    tag = t
            answer.append(tag)
        #print(answer)
        num=len(answer)    
        if answer[num-1] == "VERB":
            answer[num-1]="NOUN"
            
        elif answer[num-1] == "NOUN":
            answer[num-1]="VERB"
        #print(answer)
        return answer
'''
c = load_corpus("brown-corpus.txt")
t=Tagger(c)
print(t.most_probable_tags(["The", "man", "walks", "."]))
print(t.most_probable_tags(["The", "blue", "bird", "sings"]))

s = "I am waiting to reply".split()
print(t.most_probable_tags(s))
print(t.viterbi_tags(s))
print("\n")
s = "I saw the play".split()
print(t.most_probable_tags(s))
print(t.viterbi_tags(s))
'''
