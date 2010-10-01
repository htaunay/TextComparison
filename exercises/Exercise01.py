################################################################################
# Exercise for NLP and Python pratice
# Developed by Henrique Taunay
################################################################################

import nltk
from nltk.probability import FreqDist
from nltk.book import text7

# Creating main text object based on the Wall Street Journal corpora
# Setting all words to lowercase and removing non-alphabetical entrys
myText = [ word.lower() for word in text7 if word.isalpha() ]

# Creating text object based on myText, without repetitions
myTextSet = set( myText )

# Creating a frequency distribution with myText
fdMyText = FreqDist(myText)

# Creating histogram, and copying to file, in order of appearance
histogram = [ "%s - %s" % ( word, fdMyText[word] ) for word in myTextSet ]

fileObj = open("histogram.txt","w")
for wordInfo in histogram:
	fileObj.write("%s\n" % (wordInfo) )
fileObj.close()

# Creating sorted list of the most frequent words, to the less frequent words,
# of the reuters text and copying to file
sortedList = fdMyText.keys()

fileObj = open("sortedHistogram.txt","w")
for word in sortedList:
	fileObj.write("%s - %d\n" % (word, fdMyText[word]) )
fileObj.close()

# Only showing 50 most frequent words in plot because of limited monitor space
fdMyText.plot(50)
