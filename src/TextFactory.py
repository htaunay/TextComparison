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
	#  as without numeric values.
	def getNormalizedText( self, text ):
		nText = [ word.lower() for word in text if word.isalpha() ]
		return nText
		
	# Receives a file path, which contains a list of links to several news articles.
	#  Each of the articles get cleaned with the nltk html parser
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
		
	# Receives a Reuters category and a size, and returns a list of the first
	#  texts of the given category. If size > length of the categories, the list
	#  will have 'length' entrys, otherwise, it will have 'size' entrys.
	# If you wish to have the text normalized, set True to the third parater. By
	#  default the text isn't normalized.
	def getReutersTexts( self, category, size, normalize = False ):
		i = 0
		text = []
		reuters = nltk.corpus.reuters
	
		while i < size and i < len( reuters.fileids( category ) ):
			if not normalize:
				text.insert( i, reuters.words( reuters.fileids( category )[i] ) )
			else:
				text.insert( i, 
				self.getNormalizedText( reuters.words( reuters.fileids( category )[i] ) ) )
				
			i += 1
	
		return text
		
################################################################################
### Auxiliary Classes ###
################################################################################

### HtmlTextOptimizer ###

class HtmlTextOptimizer:
	
	# Receives a raw text sample normally obtained by a html parser, probably
	#  containg several unwanted content like: comments, advertising, links;
	#  and returns what PROBABLY is the main text o the sample.
	# This method still has to mature A LOT. I have had positve results with
	#  some cases, but also disastrous results in others.
	# The nullLimit parameter defines how many null characters ('','\n') in a 
	#  sequence are oficialy considered block separators.
	# The linelimit parameter defines how many characters in one line are
	#  necessary for considering that his line isn't unwanted content.
	# The contentlimit parameter defines how many characters in a block (between
	#  nulllimits) are necessary to be considered a relevant block of text.
	def cleanHtml( self, rawText, nullLimit = 5, lineLimit = 160, 
											contentLimit = 480 ):
		nullCount = 0
		contentCount = 0
		
		lineText = ''
		cleanText = ''
		
		for char in rawText:
			lineText += char
			contentCount += 1
			
			if char == '\n':
				if len( lineText ) >= lineLimit:
					cleanText += lineText
				lineText = ''
				
			if char == ' ' or char == '\n':
				nullCount += 1
			else:
				nullCount = 0
				
			if nullCount == nullLimit:
				if contentCount >= contentLimit: 
					return cleanText
					
				contentCount = 0
				nullCount = 0
				cleanText = ''
				
		return ''
	
	# Receives a url address, as well as a data path, and returns a clean
	#  text sample from the given address. For optimization of loading time,
	#  every time a new address in opened, the clean text is saved in a
	#  cache folder. If the same address is requested in the future, the text
	#  will be loaded from the file, minimizing the need for web access. 
	def getUrlText( self, url, dataPath ):
		
		fileDir = os.path.dirname( dataPath )
		if os.path.exists( str(fileDir + "/cache") ) == False:
			os.mkdir( str(fileDir + "/cache") )
		
		urlHash = hash( url )
		filePath = str( fileDir + "/cache/" + str(urlHash) )
		
		if os.path.exists( filePath ) == True:
			fileObj = open( filePath ,'r')
			text = fileObj.read()
			fileObj.close()
		else:
			html = urlopen( url ).read()
			raw = nltk.clean_html( html )
			text = self.cleanHtml( raw )
			if( len(text) != 0 ):
				fileObj = open( filePath ,'w')
				fileObj.write( text )
				fileObj.close()
			
		return text
		
		
