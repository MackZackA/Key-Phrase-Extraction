#!/usr/bin/python3

# import libraries

from __future__ import absolute_import
from __future__ import print_function
import operator
import nltk
import string
import sys
import re
import six
from six.moves import range
# read the file from the msa e directory as the first parameter

f = open(sys.argv[1])

# read the other three transcripts
f2 = open(sys.argv[2])
f3 = open(sys.argv[3])
f4 = open(sys.argv[4])


# get the customized inputs for minimum character length, maximum word length, and number of top n words to extract
minmum_character_length = int(sys.argv[5])
maximum_words_length = int(sys.argv[6])
top_n = int(sys.argv[7])

# Preprocessing: if there is additional newline characters, replace it with a space-kill the empty lines
# read the whole script as a long string
open_text = f.read().replace("\n", " ")
open_transcript1 = f2.read().replace("\n", " ")
open_transcript2 = f3.read().replace("\n", " ")
open_transcript3 = f4.read().replace("\n", " ")
# open_text = f.read()

def isPunct(word):
  return len(word) == 1 and word in string.punctuation

def isNumeric(word):
  try:
    float(word) if '.' in word else int(word)
    return True

  except ValueError:
    return False

# the threshold values collected from the user inputs
def threshold(phrase, min_char_length, max_words_length):
  # set a threshold value for the minimum character length a phrase has to have
  if len(phrase) < min_char_length:
    return 0 # if the phrase is too short then it is unable to pass

  # split the phrase to see if its number of words surpasses the maximum limit
  wordlist = phrase
  if len(wordlist) > max_words_length:
    return 0

  # check if the phrase has at least one alpha character
  digits = 0
  alpha = 0
  for i in range(0, len(phrase)):
    if phrase[i].isdigit():
      digits += 1
    elif phrase[i].isalpha():
      alpha += 1

  # checking if there is at least one character
  if alpha == 0:
    return 0

  # a phrase must have more alpha characters than digits
  if digits > alpha:
    return 0
  return 1


# Implementation of RAKE algorithm
class RakeKeywordExtractor:
  def __init__(self):
    self.stopwords = set(nltk.corpus.stopwords.words())
    self.top_fraction = 1 # consider top third candidate keywords by score

  def _generate_candidate_keywords(self, sentences, min_char_length = 1, max_words_length = 5):
    phrase_list = []
    for sentence in sentences:
      words = ["|" if x in self.stopwords else x for x in nltk.word_tokenize(sentence.lower())]

      phrase = []
      for word in words:
        if word == "|" or isPunct(word):
          # hey there are modifications here
          if len(phrase) > 0 and threshold(phrase, min_char_length, max_words_length):
            phrase_list.append(phrase)
            phrase = []
        else:
          phrase.append(word)

    return phrase_list


  def _calculate_word_scores(self, phrase_list):
    word_freq = nltk.FreqDist()
    word_degree = nltk.FreqDist()
    for phrase in phrase_list:
      degree = len(list([x for x in phrase if not isNumeric(x)])) - 1
      for word in phrase:
        word_freq[word] += 1
        word_degree[word] += degree # other words
    for word in list(word_freq.keys()):
      word_degree[word] = word_degree[word] + word_freq[word] # itself
    # word score = deg(w) / freq(w)
    word_scores = {}

    for word in list(word_freq.keys()):
      word_scores[word] = word_degree[word] / word_freq[word]

    return word_scores


  def _calculate_phrase_scores(self, phrase_list, word_scores):
    phrase_scores = {}
    for phrase in phrase_list:
      phrase_score = 0
      for word in phrase:
        phrase_score += word_scores[word]
      phrase_scores[" ".join(phrase)] = phrase_score

    return phrase_scores


  def extract(self, text, incl_scores=False):
    sentences = nltk.sent_tokenize(text)
    # modify the minimum character length and maximum words length here. I will recommend minimum_character_length = 1, maximum_words_length = 3.
    phrase_list = self._generate_candidate_keywords(sentences, minmum_character_length, maximum_words_length)
    word_scores = self._calculate_word_scores(phrase_list)
    phrase_scores = self._calculate_phrase_scores(
      phrase_list, word_scores)

    sorted_phrase_scores = sorted(iter(phrase_scores.items()),
      key = operator.itemgetter(1), reverse=True)

    n_phrases = len(sorted_phrase_scores)

    if incl_scores:
      return sorted_phrase_scores[0:int(n_phrases/self.top_fraction)]

    else:
      return [x[0] for x in sorted_phrase_scores[0:int(n_phrases/self.top_fraction)]]



def test():
  rake = RakeKeywordExtractor()
  # extract the output as a list of tuples: the tuples are all pairs of phrases and their values
  keywords = rake.extract(open_text, incl_scores=True)

  # sort the list of tuple by the values of each tuple, the tup[1]
  processed_keywords = sorted(keywords, key=lambda tup: tup[1])


  '''
  
  # FOR DEBUGGING, print out the whole list of extracted phrases, sorted by weighted values in descending sequence
  print("Print out the whole list of extracted phrases: ")
  print(processed_keywords) 
  print("End of Debugging")

  '''

  #retrieve the top n words from the list, n is accessed as the last user input
  val = -1 * top_n
  output = processed_keywords[val:]
  #  output_with_values = [tup[0] for tup in processed_keywords]
  output_without_values = [tup[0] for tup in output]

  # printinput filename
  print("Input File: ", sys.argv[1])

  print()
  # print the top n most important key-word phrases in descending order
  sent_to_printout = 'The top ' + str(top_n) + ' most important phrases are: '
  print(sent_to_printout, output_without_values)

  print()
  # print the full list, from highest value to the lowest
  # print("The full list: ", processed_keywords[::-1])

  # the dictionary that stores the top n phrases
  top_dict = {}
  for elem in output_without_values:
    output = str(elem)
    top_dict[elem] = 0
  print(output, end=' | ')

  for elem in top_dict:
    if elem in open_transcript1:
      top_dict[elem] += 1

    if elem in open_transcript2:
      top_dict[elem] += 1

    if elem in open_transcript3:
      top_dict[elem] += 1

  print()
  print()

  # print out the dictionary after collecting frequencies from the transcripts
  print("The frequencies of phrases in the transcripts are:")
  print(top_dict)

  # generate a list of tuples
  top_listTuple = [(ki, top_dict[ki]) for ki in top_dict.keys()]

  # sorted by frequencies
  # since the weighted values of some phrases are equal, it is natural that every time the sequence of these phrases would vary
  sorted_list = sorted(top_listTuple, key=lambda tup: tup[1])

  print()
  print()

  # print out the ranking for these top n words
  i = 0
  for x in reversed(sorted_list):
    i += 1
    print(x[0], i)




if __name__ == "__main__":

  test()
