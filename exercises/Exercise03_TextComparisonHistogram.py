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
import matplotlib.pyplot as plot

### Internal Librarys ###
from TextFactory import TextFactory
from TextComparisonUtils import TextComparisonUtils

### Main Execution ###

tf = TextFactory()

# Concatenates each generated text into one main text list.
mainList = []
mainList += tf.getReutersTexts( 'trade', 500, True )
mainList += tf.getReutersTexts( 'interest', 500, True )

tcu = TextComparisonUtils()

# Removing stopwords from each of the texts.
for l in mainList:
	mainList[ mainList.index( l ) ] = tcu.removeStopwords( l )
	
# Lemmatizing all entrys in all list in the mainList utilizing the WordNet
#  lemmatizer method, encapsulated by the TextComparisonUtils class.
for l in mainList:
	mainList[ mainList.index(l) ] = tcu.lemmatizeText( l )

# Creating a list of frequency distributions of each of the text in the
#  mainList, then sorting them alphabetically.
# I stopped using 'list.index(l)' and started using the good old fashioned i=0
#  and i++, because the fucking 'index' function is unstable and made me lose
#  hours of work over a counter that doesn't know how to count >(
i = 0
freqDistList = []
for l in mainList:
	fd = nltk.probability.FreqDist( l )
	sample = sorted( set( l ) )
	sortedFreqDist = [ ( word, fd[word] ) for word in sample ]
	freqDistList.insert( i, sortedFreqDist )
	i += 1

# Creating and populating a similarity list, containing all of the cosine
#  similarity results calculated between all of the texts in the mainlist.
pos = 0
l = 0
similarityList = []
while l < len( freqDistList ):
	i = l + 1
	while i < len( freqDistList ):
		if i != l:

			intersection = tcu.getTextIntersection( mainList[l], mainList[i] )
			similarity = tcu.calcCosineSimilarity( freqDistList[l], 
												   freqDistList[i], 
												   intersection )
				
			similarityList.insert( pos, similarity )
			
		pos += 1
		i += 1
	l += 1
		
# Removes from the similarityList, values that results came from invalid text
#  samples, that ALWAYS presented similarities below the expected threshold
tcu.cleanInvalidData( similarityList )
	
# Creating a plot figure obejct and setting as a subplot a histogram object
#  constructed with the cosine similarty results of the last step.
fig = plot.figure()
ax = fig.add_subplot( 111 )
ax.hist( similarityList, 50 )

# Customizing the histogram configuration
ax.set_xlabel( 'Similarity' )
ax.set_ylabel( 'Frequency' )
ax.set_xlim( 0, 1 )
ax.set_ylim( 0, len( similarityList)/9 )
ax.grid( True )

plot.title( 'Trade + Interest' )
plot.show()

