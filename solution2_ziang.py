#!/usr/bin/python3

import nltk
import sys
import string

from nltk.collocations import *

# reading the file from input, removing empty lines
f = open(sys.argv[1])

# these three parameters are used to collect inputs of the three transcripts
f2 = open(sys.argv[2])
f3 = open(sys.argv[3])
f4 = open(sys.argv[4])
top_n = int(sys.argv[5])

open_transcript1 = f2.read().replace("\n", " ")
open_transcript2 = f3.read().replace("\n", " ")
open_transcript3 = f4.read().replace("\n", " ")

open_text = f.read().replace("\n", " ")

# the list that stores all the tokens in the script (the source of key phrases)
bigfreakinglist = []

# tokenizing the text, which is a long string, into a list of sentences
sentences = nltk.sent_tokenize(open_text)
for sent in sentences:
  
  # word_list = nltk.wordpunct_tokenize(sent)
  word_list = nltk.word_tokenize(sent)
  bigfreakinglist += word_list 

# find the most associated collocations of bigrams and trigrams from NLTK database
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

# filter out bigrams that appear more than 3 times
finder = BigramCollocationFinder.from_words(bigfreakinglist)
finder.apply_freq_filter(3)

# filter out trigrams that appear more than 3 times
tri_finder = TrigramCollocationFinder.from_words(bigfreakinglist)
tri_finder.apply_freq_filter(3)

# return a list of top 30 tuples of bigrams and trigrams with the highest pointwise mutual information (PMI) 
result1 = finder.nbest(trigram_measures.pmi, top_n)
result2 = tri_finder.nbest(bigram_measures.pmi, top_n)

# create a dictionary that stores the top 20 most important two-word phrases as keys, with default phrase count 0
phrase_dict = {}
print("The top 10 most important two-word phrases are:")
for tup in result1:
  output = str(tup[0]) + ' ' + str(tup[1])
  phrase_dict[output] = 0
  print(output, end=' | ')

print()
print()

# create a dictionary that stores the top 20 most important three-word phrases as keys, with default phrase count 0
print("The top 10 most important three-word phrases are:")
for tup in result2:
  output = str(tup[0]) + ' ' + str(tup[1]) + ' ' + str(tup[2])
  phrase_dict[output] = 0
  print(output, end=' | ')


# now looping through all the three transcripts, which are read as three long strings, to calculate the frequency of the phrases
for utterance in phrase_dict:
  if utterance in open_transcript1:
    phrase_dict[utterance] += 1

for utterance in phrase_dict:
  if utterance in open_transcript2:
    phrase_dict[utterance] += 1

for utterance in phrase_dict:
  if utterance in open_transcript3:
    phrase_dict[utterance] += 1

print()
print()

# print out the dictionary after collecting frequencies from the transcripts
print("The frequencies of phrases in the transcripts are:")
print(phrase_dict)

# generate a list of tuples 
top_listTuple = [(ki, phrase_dict[ki]) for ki in phrase_dict.keys()]

# sorted by frequencies
# since there are more than 1 phrase with 0 count, it is natural that every time the generated list is different
sorted_list = sorted(top_listTuple, key=lambda tup: tup[1])


print()
print()

# print out the ranking for these top n words
i = 0
for x in reversed(sorted_list):
  i += 1
  print(x[0], i)




