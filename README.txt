The solution is comprised of two scripts: solution1_ziang.py and solution2_ziang.py.

For solution1_ziang.py:
Algorithm: RAKE

Dependencies: six, re, sys, string, nltk, operator, __future__

Language: Python 3

Instructions:
To run the script on Linux:
python3 solution1_ziang.py (the text from which the phrases are extracted) (analyzed transcript 1) (analyzed transcript 2) (analyzed transcript 3) (minimum character length) (maximum words length) (number of top n phrases you would like to extract)
For example: "python3 solution1_ziang.py script.txt transcript_1.txt transcript_2.txt tra nscript_3.txt 1 3 100"



For solution2_ziang.py:
Mechanism: PMI (Pointwise Mutual Information)

Dependencies: NLTK Collocations, bigram package, trigram package

Running the script:
python3 solution2_ziang.py (the text from which the phrases are extracted) (analyzed transcript 1) (analyzed transcript 2) (analyzed transcript 3) (number of top n phrases you would like to extract)
For example: "python3 solution2_ziang.py script.txt transcript_1.txt transcript_2.txt tran script_3.txt 50"


RAKE:
This script implements RAKE algorithm, realized by NLTK package.
The RAKE algorithm specifically focuses on the extracting significant features from mundane, ordinary expressions (e.g. is, an, be, the, etc) in the single text document. Slightly relying on external features and evening training, it outperforms TextRank and K-MM method with its comparatively less storages and efficencies when implementing at an industrial scale. It prefers longer expressions, assigning weighted values assigned to each word and eventually summing them up to the total weights of the phrases. However, the contents it extracts are highly text-dependent, i.e., so exclusive that they may not serve as ideal references for key phrases in texts whose topics are not closely related. As evidenced from the output, the generated features serve well in offering a comprehensive knowledge of the analyzed script.txt, but behave poorly in capturing core phrases in other three transcripts. Yet I would still believe it's idea candidate for analyzing single text.

Observation: when the number of extracted phrases is between 0 to 20, it shows the names of organization and descriptions of actions and products from the file; when the number lies between 20 and 50, you are able to see more detailed scenario; the ideal number of extraction may be around 80.

*** Note that the sequence of phrases may ary somehow. It is natural because the limited number of extraction leads to many of those utterances having the same weighted values, by which they are sorted. (To see the full list of extracted expressions, remove the comments between 162 and 169)


NLTK Collocations:
Using the collocation databases of NLTK, I build the bigram and trigram associative models, using thresholds to yield phrases trustworthy frequencies, then sort by their PMI. The higher the PMI, the most credible the key phrases are. The extracted phrases are able to rank themselves based on the analyzed transcripts conspicuously, given larger number of extraction.
