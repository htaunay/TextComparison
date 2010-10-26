################################################################################
# Exercise for NLP and Python pratice
# Comparison between two different groups of text
# Rio de Janeiro, 26/08/2010
# Developed by Henrique Taunay
################################################################################

### Add src directory to PYTHONPATH ###
import sys
sys.path.append( "../src" )

### External Librarys ###
import nltk
from matplotlib import pyplot
from hcluster import pdist, linkage, dendrogram

### Internal Librarys ###
from TextFactory import TextFactory
from TextComparisonUtils import TextComparisonUtils

### Main Execution ###

tf = TextFactory()

# Concatenates each generated text into one main text list.
mainList = []
mainList += tf.getReutersTexts( 'trade', 10, True )
mainList += tf.getReutersTexts( 'interest', 10, True )

tcu = TextComparisonUtils()

# Removing stopwords from each of the texts.
for l in mainList:
	mainList[ mainList.index( l ) ] = tcu.removeStopwords( l )

# Lemmatizing all entrys in all list in the mainList utilizing the WordNet
#  lemmatizer method, encapsulated by the TextComparisonUtils class.
for l in mainList:
	mainList[ mainList.index(l) ] = tcu.lemmatizeText( l )
	
# Creating a list of all words that exist in all and any texts present in the
#  mainList. The words are ordered alphabetically, and there are no repititions.
# This set represents the 'dimensions' of the space used to calculate the
#  distance(similarity) between texts.
wordSet = tcu.createWordSet( mainList )

# Creating a list of frequency distributions of each of the text in the
#  mainList.
# I stopped using 'list.index(l)' and started using the good old fashioned i=0
#  and i++, because the fucking 'index' function is unstable and made me lose
#  hours of work over a counter that doesn't know how to count >(
i = 0
freqDistList = []
for l in mainList:
	fd = nltk.probability.FreqDist( l )
	freqDistList.insert( i, fd )
	i += 1

# Creating a list of text positions in the 'space', determined by all the
#  existing words. All words that dont exist in a text receive the value 0. The
#  ones that do, receive the value calculated previously in the FreqDist.
textPositionList = []
for f in freqDistList:
	textPositionList.append( tcu.populateTextPosition( f, wordSet ) )
	
# Creating a distribution of all text positions, followed by the calculation
#  of the distances of all the texts between themselves.
distribution = pdist( textPositionList )
textLinks = linkage( distribution )

# Drawing a plot containing a dendrogram, using the links(distances) between
#  the positions of the sample texts.
dendrogram( textLinks )
pyplot.title( "Dendrogram" )
pyplot.show()

