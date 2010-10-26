################################################################################
# Exercise for NLP and Python pratice
# Text comparisson utility functions.
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
		 return [ word for word in text if word not in nltk.corpus.stopwords.words('english') or len(word) < 2 ]
		 
	# Receives a text, and returns all of its entrys lemmatized by the
	#  WordNet lemmatizer method.
	def lemmatizeText( self, text ):
		lemmatizer = nltk.WordNetLemmatizer()
		ltext = []
		i = 0
		
		for word in text:
			if len( word ) > 1:
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
	#  and returns a new frequency distribution with only the words also included
	#  in the given intersection list
	def removeNonIntersections( self, freqDist, intersection ):
		i = 0
		newFD = []
	
		for fd in freqDist:
			if intersection.count( fd[0] ) != 0:
				newFD.insert( i, fd )
				i += 1
			
		return newFD
		
	# Receives a frequency distribution, and a list of keywords. Returns the
	#  same frequency distribution, but with all the keywords present in it
	#  (if any), re-scaled according to the given scale factor.
	def redefineScales( self, fd, keywords, scale = 3 ):
		newFd = []
		for tupl in fd:
			if tupl[0] in keywords:
				newFd += [( tupl[0], tupl[1]*scale )]
			else:
				newFd += [( tupl[0], tupl[1] )]
				
		return newFd

	# Calculates the dot operation between two lists, or nx1 matrixes.
	def fdDot( self, A, B ):
		if len( A ) != len( B ):
			raise DotCalculationError( 'The Dot operation connto be performed' +
									   'between two lists of different sizes!' )
	
		pot = 0	
		for n in A:
			pot += n[1] * B[ A.index( n ) ][1]
		
		return pot		

	# Receives two lists representing text frequency distributions, and returns a
	#  value varying from 0 to 1, representing Theta, the cosine similarity between
	#  the given texts
	def calcCosineSimilarity( self, fd1, fd2, intersection ):

		if len( intersection ) == 0:
			return 0
		
		cleanFD1 = self.removeNonIntersections( fd1, intersection )
		cleanFD2 = self.removeNonIntersections( fd2, intersection )
			
		top = self.fdDot( cleanFD1, cleanFD2 )
		bottom = math.sqrt( self.fdDot( fd1, fd1 ) ) * math.sqrt( self.fdDot( fd2, fd2 ) )
		
		if (top/bottom) < 0:
			print 'C1 - ', cleanFD1
			print 'C2 - ', cleanFD2
			x = raw_input('Ok')
		
		return ( top/bottom )
		
	# Receives a similarityList, and returns the number of texts(depth) that
	#  were necessary to generate a similarityList of such size. In other words,
	#  n texts generate n(n-1)/2 similarity results. This method returns n from
	#  numResults.
	def findSimilarityListDepth( self, similarityList ):
		stack = 1
		counter = 2
		listSize = len( similarityList )
		
		if listSize <= 0:
			return -1
		
		while True:
			if stack == listSize:
				return counter
			elif stack >= listSize:
				return -1
				
			stack += counter
			counter += 1
	
	# Receives a list of similaries regarding one specific text, and returns if 
	#  a text sample is invalid, by vrifying if any of the comparisons of the
	#  given text between the rest of the samples generated at least one
	#  acceptable(above threshold) result.
	def isTextInvalid( self, textSimilarityList, threshold = 0.2 ):
		
		for s in textSimilarityList:
			if s > threshold:
				return False
				
		return True
		
	
	# Receives a list of similarities, and removes data from it, if
	#  considered to be invalid. This method MODIFIES the similarityList
	#  parameter, and is very specific for the type of data it receives,
	#  since it is necessary to decompose the given list into the original
	#  order of the similarity calculation step. This process can not be done
	#  in such step, because: you first need to calculate all the similarites
	#  before difining if it is invalid or not; and not necessarily everyone
	#  may want his/her invalid data cleaned.
	def cleanInvalidData( self, similarityList ):
	
		depth = self.findSimilarityListDepth( similarityList )
		if depth == -1:
			return
		
		auxSimList = []
		auxPosList = []
		removalList = []
		num = 0
		
		while num < depth:
			
			auxSimList[:] = []
			auxPosList[:] = []
			
			height = num
			width = depth - 2

			totalCounter = num - 1
			if totalCounter < 0:
				totalCounter = 0
				
			while height != 0:
				auxSimList.append( similarityList[totalCounter] )
				auxPosList.append( totalCounter )
				totalCounter += width
				height -= 1
				width -= 1
				
			if num != 0:
				totalCounter += 1
			
			for i in range( depth - (num + 1) ):
				auxSimList.append( similarityList[totalCounter] )
				auxPosList.append( totalCounter )
				totalCounter += 1
				
			if self.isTextInvalid( auxSimList ):
				removalList[len(removalList):] = auxPosList
			
			num += 1
			
		for j in range( len(removalList) ):
			del  similarityList[ removalList.pop() ]
			
	# Receives a text, and returns a set of it, sorted.
	def sortAndSet( self, text ):
		counter = {}
		for i in text:
			try: counter[i] += 1
			except KeyError: counter[i] = 1
			
		ss = counter.keys()
		ss.sort()
		
		tss = {}
		
		for w in ss:
			tss[w] = 0
		
		return tss
			
	# Receives a list of texts, and returns a ordered set of all the words
	#  present in them.
	def createWordSet( self, textList ):
		wordSet = []
		for l in textList:
			wordSet[len(wordSet):] = l
			
		wordSet = self.sortAndSet( wordSet )
		
		return wordSet
		
	# Receives a frequency distribution regarding a text, and a word set.
	# Returns a text position in the space represented by n dimensions (n beign
	#  the number of words in the word set), of which coordinates are the
	#  words frequencies.
	def populateTextPosition( self, freqDist, wordSet ):
		tp = []
		for w in wordSet:
			tp.append( freqDist[w] )
			
		return tp
				
			
