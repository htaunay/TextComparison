################################################################################
# Exercise for NLP and Python pratice
# Creating a comparison table between several text sources
# Rio de Janeiro, 26/08/2010
# Developed by Henrique Taunay
################################################################################

import nltk
import math
import Tkinter as tk
from nltk.corpus import reuters
from nltk.corpus import stopwords
from nltk.probability import FreqDist

### Global constants ###
CATEGORY_SIZE  = 5
NUM_CATEGORIES = 4
NUM_TEXTS      = CATEGORY_SIZE * NUM_CATEGORIES

### Module Methods ###

# Receives a word list, and returns it with all words in lower case, as well
# as without numeric values.
def getNormalizedText( text ):
	nText = [ word.lower() for word in text if word.isalpha() ]
	return nText
	
# Receives a Reuters category and a size, and returns a list of the first
# texts of the given category. If size > length of the categories, the list
# will have 'length' entrys, otherwise, it will have 'size' entrys.
# If you wish to have the text normalized, set True to the third parater. By
# default the text isn't normalized.
def generateTextList( category, size, normalize = False ):
	i = 0
	text = []
	
	while i < size and i < len( reuters.fileids( category ) ):
		if not normalize:
			text.insert( i, reuters.words( reuters.fileids( category )[i] ) )
		else:
			text.insert( i, 
			getNormalizedText( reuters.words( reuters.fileids( category )[i] ) ) )
		i += 1
	
	return text
	
# Receives a text, and returns it without any stopwords(in english).
def removeStopwords( text ):
     return [ word for word in text if word not in stopwords.words('english') ]
	
# Receives two texts and returns a ordered list of words in common of both
def getTextIntersection( t1, t2 ):
	i = 0
	ss1 = sorted( set( t1 ) )
	ss2 = sorted( set( t2 ) )
	intersectionList = []
	
	for word in ss1:
		if ss2.count( word ) != 0:
			intersectionList.insert( i, word )
			i += 1
			
	return intersectionList

# Receives a frequency distribution object, and a list of intersection words,
# and returns a new frequency distribution with only the words also included
# in the given intersection list
def removeNonIntersections( freqDist, intersection ):
	i = 0
	newFD = []
	
	for fd in freqDist:
		if intersection.count( fd[0] ) != 0:
			newFD.insert( i, fd )
			i += 1
			
	return newFD

# Calculates the dot operation between two lists, or nx1 matrixes.
def fdDot( A, B ):
	if len( A ) != len( B ):
		return -1
	
	pot = 0	
	for n in A:
		pot += n[1] * B[ A.index( n ) ][1]
		
	return pot		

# Receives two lists representing text frequency distributions, and returns a
# value varying from 0 to 1, representing Theta, the cosine similarity between
# the given texts
def calcCosineSimilarity( fd1, fd2, intersection ):

	if len( intersection ) == 0:
		return 0
		
	cleanFD1 = removeNonIntersections( fd1, intersection )
	cleanFD2 = removeNonIntersections( fd2, intersection )
			
	top = fdDot( cleanFD1, cleanFD2 )
	bottom = math.sqrt( fdDot( fd1, fd1 ) ) * math.sqrt( fdDot( fd2, fd2 ) )
	
	return top/bottom
	
# UI intended method. Receives a data list, and formats and prints it into
# a window.
def makeTable( dataList ):

    mainString = ""
    for table in dataList:
    	for entry in table:
        	mainString += entry
        mainString += '\n'
    
    return mainString

### Main Execution ###
	
# Creating texts object based on the Reuters corpora.
# Five text samples were selected from four categories each.
# The categories are 'cocoa', 'gold', 'potato', 'tea'.
cocoaList  = generateTextList( 'cocoa',  CATEGORY_SIZE, True )
goldList   = generateTextList( 'gold',   CATEGORY_SIZE, True )
potatoList = generateTextList( 'potato', CATEGORY_SIZE, True )
teaList    = generateTextList( 'tea',    CATEGORY_SIZE, True )

# Concatenates each generated text into one main text list.
mainList = []
mainList += cocoaList
mainList += goldList
mainList += potatoList
mainList += teaList

# Removing stopwords from each of the texts.
for l in mainList:
	mainList[ mainList.index( l ) ] = removeStopwords( l )

# Lemmatizing all entrys in all list in the mainList utilizing the WordNet
# lemmatizer method.
lemmatizer = nltk.WordNetLemmatizer()
for l in mainList:
	mainList[ mainList.index(l) ] = [ lemmatizer.lemmatize(word) for word in l ]

# Creating a list of frequency distributions of each of the text in the
# mainList, then sorting them alphabetically
freqDistList = []
for l in mainList:
	fd = FreqDist( l )
	sample = sorted( set( l ) )
	sortedFreqDist = [ ( word, fd[word] ) for word in sample ]
	freqDistList.insert( mainList.index(l), sortedFreqDist ) 

# create the main window
root = tk.Tk()

# Populates a data list, that will be used and formated into a window view.
dataList = []
for i in range(21):
	line = []
	for j in range(21):
		# First cell in the table
		if i == 0 and j == 0:
			line.insert( j, 'Texts'.rjust(5) )
			
		# First column elements
		elif i == 0 and j != 0:
			line.insert( j, str('T{0}').format(j).rjust(8) )
			
		# First line elements
		elif i != 0 and j == 0:
			line.insert( j, str('T{0}').format(i).rjust(5) )
		
		# Calculates the cosine similarity between texts, and adds the result
		# to the data list	
		else:
			line.insert( j, 
			str( calcCosineSimilarity( freqDistList[i-1], freqDistList[j-1], 
			getTextIntersection( mainList[i-1], mainList[j-1] ) ) )[0:5].rjust(8) )
	
	dataList.insert( i, line )
		
table = makeTable( dataList )

# for tables use a monospaced font like courier
myfont = ( 'courier', 10 )
# create a label showing the table using myfont
# with red characters on yellow background
label = tk.Label(root, text=table, font=myfont, fg='green', bg='black' )
# position the label
label.pack()

# start the event loop
root.mainloop()

