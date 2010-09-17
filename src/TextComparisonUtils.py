################################################################################
# Exercise for NLP and Python pratice
# Text comparisson Utility Functions
# Rio de Janeiro, 17/09/2010
# Developed by Henrique Taunay
################################################################################

import nltk
import math

################################################################################
### Main Class ###
################################################################################

class TextComparisonUtils:

	# Receives a text, and returns it without any stopwords(in english).
	def removeStopwords( self, text ):
		 return [ word for word in text if word not in nltk.corpus.stopwords.words('english') ]
		 
	# Receives a text, and returns all of its entrys lemmatized by the
	# WordNet lemmatizer method.
	def lemmatizeText( self, text ):
		lemmatizer = nltk.WordNetLemmatizer()
		ltext = []
		i = 0
		
		for word in text:
			ltext.insert( i, lemmatizer.lemmatize(word) )
			i += 1
		
		return ltext
	
	# Receives two texts and returns a ordered list of words in common of both
	def getTextIntersection( self, t1, t2 ):
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
	def removeNonIntersections( self, freqDist, intersection ):
		i = 0
		newFD = []
	
		for fd in freqDist:
			if intersection.count( fd[0] ) != 0:
				newFD.insert( i, fd )
				i += 1
			
		return newFD
		
	#TODO
	def redefineScales( self, fd, keywords ):
		newFd = []
		for tupl in fd:
			if tupl[0] in keywords:
				newFd += [( tupl[0], tupl[1]*2 )]
			else:
				newFd += [( tupl[0], tupl[1] )]
				
		return newFd

	# Calculates the dot operation between two lists, or nx1 matrixes.
	def fdDot( self, A, B ):
		if len( A ) != len( B ):
			return -1
	
		pot = 0	
		for n in A:
			pot += n[1] * B[ A.index( n ) ][1]
		
		return pot		

	# Receives two lists representing text frequency distributions, and returns a
	# value varying from 0 to 1, representing Theta, the cosine similarity between
	# the given texts
	def calcCosineSimilarity( self, fd1, fd2, intersection ):

		if len( intersection ) == 0:
			return 0
		
		cleanFD1 = self.removeNonIntersections( fd1, intersection )
		cleanFD2 = self.removeNonIntersections( fd2, intersection )
			
		top = self.fdDot( cleanFD1, cleanFD2 )
		bottom = math.sqrt( self.fdDot( fd1, fd1 ) ) * math.sqrt( self.fdDot( fd2, fd2 ) )
	
		return ( top/bottom )
		
