# The code provides fesility to extract the important keywords from a given text story. 

# Steps I have taken 

# 1) cleaning process (Removing unnecessary things, punctuations, html tags etc) and removing redundant entries. 
# 2) Removing the stopping words. For example, a, an, the etc. 
# 3) Tokenize the stories using nltk framework. 
# 4) First collected all those keywords mentioned in " " form. Moreover, taken sentences as well in " " form. 
# 5) Now comes the crucial part, for giving importance weight to a keyword. I used "tf idf algorithm" - https://en.wikipedia.org/wiki/Tf%E2%80%93idf 
# 6) The proposed method requires two values a) tf -term frequency  and b) idf- inverse document frequency. It uses these to formulate a statistic tf-idf, based on that I gives importance to the keywords. 

 
# The code supports functionality for english language only. There are certain functions to support hindi language too but, it's not complete yet, support for hindi language is in process.
      
# Written by Maunil Vyas - vyasmaunil33@gmail.com      
from __future__ import division
import numpy as np
import operator
import codecs
import pandas as pd
import csv
import re
import nltk
from rake_nltk import Rake
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import math
#from nltk.tokenize import sent_tokenize, word_tokenize
 

def term_frequency(index, data_set):
    dic = {}
    
    for i in data_set[index]:
    	dic[i] = 0
    
    for i in data_set[index]:
    	if (dic[i] == 0):
    	    dic[i] = float(1/len(data_set[index]))
    	else: 
    	    dic[i] = dic[i] + float(1/len(data_set[index]))    	
    	
    return dic
    
def n_containing(word, data_set):
    counter = 0
    for i in data_set:
    	if word in i:
    	   counter = counter + 1
    
    return counter
    	
def inverse_term_frequency(word, eng_doc, data_set):
    return math.log(eng_doc / (1 + n_containing(word, data_set)))

def tfidf_score(index, eng_doc, data_set):
    dic = term_frequency(index, data_set)
    #print dic
    score_dic = {}
    
    for i in dic:
    	score_dic[i] = dic[i]*inverse_term_frequency(i, eng_doc, data_set)
	
    return score_dic
    		
def read_and_clean(filename):
    data = []
    eng_doc = 0
    hi_doc = 0
    file_data = csv.reader(open(filename),skipinitialspace=True)
    sortedlist = sorted(file_data, key=lambda row: row[0])
    
    #Removing empty data
    for line in sortedlist:
        if (line[3] != "" and line[1]=="english"):
		data.append(line)
		eng_doc = eng_doc + 1 
	elif (line[3] != "" and line[1]=="hindi"):
		temp = [line[0],line[1],unicode(line[2],"utf-8"),unicode(line[3],"utf-8"),line[4]]
		data.append(temp)
		hi_doc = hi_doc + 1
		
    #Removing Redudnant data with same id number 
    data1 = []
    for i in range(len(data)-1):
    	if data[i][0]!= data[i+1][0]:
    		data1.append(data[i][:])
    
    if data[len(data)-1][0]!= data[len(data)-1][0]:
    	data1.append(data[len(data)-1][:])
    			   	      	    	         	
    return data1,hi_doc,eng_doc

def remove_common_words(story,stop_words):
    filtered_story = []
    
    for w in story:
    	word = w.split(" ")
    	dump = []		
    	for k in word:
    	    if k not in stop_words:
            	dump.append(k)
        str1 = ' '.join(dump)    	
	filtered_story.append(str1)	    	
    return filtered_story

def process_the_story(story):
    #print story
    story = story.replace("</p>","").replace("<p>","").replace("\n","").replace("\s","").replace("</strong>","").replace(":","")  
    #story = story.split(":")
    story = story.split("<br/><center>")	
    story = story[0].split("<em>")
    english_stop_words = set(stopwords.words('english'))
    
    filtered_story = remove_common_words(story,english_stop_words)
    filtered_story = ''.join(filtered_story)
    filtered_story = filtered_story.lower()
    return filtered_story

def write_in_csv(data,filename):
    f = open(filename, 'w')
    with f:
    	writer = csv.writer(f)
    
    	for row in data:
        	writer.writerow(row)
    
            
def tockens(story):
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(story)	
	
    
def important_keywords(story):
    try:
    	found = (re.search('\"(.+?)\"', story).group(1))    	
    except AttributeError:
    	found = ""  
    
    return found
    
if __name__ == "__main__":
    print "Code is working!"
    data,hi_doc,eng_doc = read_and_clean("articles.csv")
    
    clean_data = []
    
    #dic = term_frequency(data[0][0],clean_data)
    
    for i in range(eng_doc):
    	clean_data.append(tockens(process_the_story(data[i][3])))
    
    print eng_doc
    exit()
    
    keys = []
    for i in range(eng_doc):
    	    key = []
    	    print i
    	    flag = 0
	    key.append(data[i][2])
	    score = tfidf_score(i, eng_doc, clean_data)
    	    sorted_x = sorted(score.items(), key=operator.itemgetter(1),reverse=True)	
     	    
     	    story = process_the_story(data[i][3])
    	    found = important_keywords(story)
    	    #imp_keys = []
            if (found!=""):
    	        found = "\"" +found +  "\""
            while (found!=""):
                #flag = 1
    		key.append(important_keywords(story))
    		story = story.replace(found,"")
    		found = important_keywords(story)
    		if (found!=""):
    			found = "\"" +found +  "\""
    			
    	    #if (flag==1):
	    #	    key.append(imp_keys)
    	    
    	    for l in range(len(sorted_x)):
    	    	key.append(sorted_x[l][0])
    	     
    	    keys.append(key) 
    
    write_in_csv(keys,"Key_Extraction.csv")	
 		    
    
    
