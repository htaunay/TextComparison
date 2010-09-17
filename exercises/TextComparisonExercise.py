################################################################################
# Exercise for NLP and Python pratice
# Creating a comparison table between several text sources
# Rio de Janeiro, 26/08/2010
# Developed by Henrique Taunay
################################################################################

### Add src directory to PYTHONPATH ###
import sys
sys.path.append( "../src" )

### External Librarys ###
import nltk
import matplotlib.pyplot as plot

### Internal Librarys ###
from TextFactory import TextFactory
from TextComparisonUtils import TextComparisonUtils

### Main Execution ###

tf = TextFactory()

# Concatenates each generated text into one main text list.
mainList = []
mainList += tf.getHtmlTexts( "../data/ibra.htmldata" )
mainList += tf.getHtmlTexts( "../data/gtx480.htmldata" )

tcu = TextComparisonUtils()

# Removing stopwords from each of the texts.
for l in mainList:
	mainList[ mainList.index( l ) ] = tcu.removeStopwords( l )

# Lemmatizing all entrys in all list in the mainList utilizing the WordNet
# lemmatizer method, encapsulated by the TextComparisonUtils class.
for l in mainList:
	mainList[ mainList.index(l) ] = tcu.lemmatizeText( l )

# Creating a list of frequency distributions of each of the text in the
# mainList, then sorting them alphabetically
freqDistList = []
for l in mainList:
	fd = nltk.probability.FreqDist( l )
	sample = sorted( set( l ) )
	sortedFreqDist = [ ( word, fd[word] ) for word in sample ]
	freqDistList.insert( mainList.index(l), sortedFreqDist ) 

#TODO
keywords = [ 'card', 'nvidia', 'core', 'ati', 'fermi', 'review', 
			 'barcelona', 'ibrahimovic', 'transfer', 'milan', 'million' ]
for l in freqDistList:
	freqDistList[ freqDistList.index(l) ] = tcu.redefineScales( l, keywords )

#TODO
pos = 0
similarityList = []
for l in freqDistList:
	lpos = freqDistList.index(l)
	i = lpos + 1
	for i in range( len(freqDistList) ):
		if i != lpos:
			similarity = tcu.calcCosineSimilarity( freqDistList[lpos], 
												   freqDistList[i], 
												   tcu.getTextIntersection( mainList[lpos], mainList[i] ) )
		
			similarityList.insert( pos, similarity )
		pos += 1
		i += 1
	
#TODO
fig = plot.figure()
ax = fig.add_subplot( 111 )
ax.hist( similarityList, 50 )

#TODO
ax.set_xlabel( 'Similarity' )
ax.set_ylabel( 'Frequency' )
ax.set_xlim( 0, 1 )
ax.set_ylim( 0, len( similarityList)/5 )
ax.grid( True )

plot.show()

