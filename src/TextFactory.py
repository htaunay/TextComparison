################################################################################
# Exercise for NLP and Python pratice
# Class for obtaining text samples from various sources
# Rio de Janeiro, 16/09/2010
# Developed by Henrique Taunay
################################################################################

import nltk
import os
from urllib import urlopen

################################################################################
### Main Class ###
################################################################################

class TextFactory:

	# Receives a word list, and returns it with all words in lower case, as well
	# as without numeric values.
	def getNormalizedText( self, text ):
		nText = [ word.lower() for word in text if word.isalpha() ]
		return nText
		
	# Receives a file path, which contains a list of links to several news articles.
	# Each of the articles get cleaned with the nltk html parser
	def getHtmlTexts( self, filePath, normalized = True ):
		fileObj = open( filePath ,"r")
		hto = HtmlTextOptimizer()
		
		textList = []
		i = 0
	
		for line in fileObj:
			raw = hto.getUrlText( line, filePath )
			text = nltk.word_tokenize(raw)
		
			if normalized == True:
				text = self.getNormalizedText( text )
			
			textList.insert( i, text )
			i += 1

		fileObj.close()
		return textList
		
################################################################################
### Auxiliary Classes ###
################################################################################

### HtmlTextOptimizer ###

class HtmlTextOptimizer:
	
	def getUrlText( self, url, dataPath ):
		urlHash = hash( url )
		fileDir = os.path.dirname( dataPath )
		
		if os.path.exists( str(fileDir + "/cache") ) == False:
			os.mkdir( str(fileDir + "/cache") )
		
		filePath = str( fileDir + "/cache/" + str(urlHash) )
		
		if os.path.exists( filePath ) == True:
			fileObj = open( filePath ,'r')
			text = fileObj.read()
		else:
			html = urlopen( url ).read()
			text = nltk.clean_html( html )
			fileObj = open( filePath ,'w')
			fileObj.write( text )
			
		fileObj.close()
			
		return text
		
		
