import math, os, pickle, re

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""

      #initialize attributes
      self.dPosFreqs = dict()
      self.dNegFreqs = dict()
      self.sPosFileName = "pos.dat"
      self.sNegFileName = "neg.dat"
      self.sTrainingDataDirectory = "movie_reviews/"
      self.sNegativeFileStarter = "movies-1"
      self.sPositiveFileStarter = "movies-5"

      #check if a cached classifier exists within the current directory
      if os.path.isfile(self.sPosFileName) and os.path.isfile(self.sNegFileName):
         print "data files found - loading to use cached values..."
         self.dPosFreqs = self.load(self.sPosFileName)
         self.dNegFreqs = self.load(self.sNegFileName)
      else:
         print "data files not found - running training..."
         self.train()

   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""
      
      #get the list of file names from the training data directory
      lFileList = []
      for fFileObj in os.walk(self.sTrainingDataDirectory):
         lFileList = fFileObj[2]
         break
      for review in lFileList:
            s = self.loadFile(self.sTrainingDataDirectory + review)
            wordslst = self.tokenize(s)
            if review[7] == "1":
                  for token in wordslst:
                        if self.dNegFreqs.has_key(token.lower().strip()):
                              self.dNegFreqs[token.lower().strip()] += 1
                        else:
                              self.dNegFreqs[token.lower().strip()] = 1
            else:
                  for token in wordslst:
                        if self.dPosFreqs.has_key(token.lower().strip()):
                              self.dPosFreqs[token.lower().strip()] += 1
                        else:
                              self.dPosFreqs[token.lower().strip()] = 1
      self.save(self.dPosFreqs,self.sPosFileName)
      self.save(self.dNegFreqs,self.sNegFileName)
                  
      #lFileList now holds a list of the filenames 
      #self.sTrainingDataDirectory holds the folder name where these files are stored

      #for each file, if it is a negative file, update the frequencies in the
      #   negative frequency dictionary.  If it is a positive file, update the 
      #   frequencies in the positive frequency dictionary.  If it is neither
      #   a postive or negative file, ignore it and move to the next file.
      #To update the frequencies for each file, you need to get the text of the
      #   file, tokenize it, then update the appropriate dictionary for those tokens.

      #for debugging purposes, it might be useful to print out the tokens and 
      #   their frequencies for both the positive and negative dictionaries

      #using the self.save method, save the frequency dictionaries to avoid extra 
      #    work in the future. The objects to save to are self.dPosFreqs and 
      #    self.dNegFreqs and the files to save to are self.sPosFileName and 
      #    self.sNegFileName
    
   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral)."""

      #get a list of the individual tokens that occur in sText
      
      #create some variables to store the positive and negative probability. The 
      # initial values for the positive and negative probabilities should be set to 0.

      #get the sum of ALL of the frequencies of the features in each document class. 
      #  This will be used in calculating the probability of each document class 
      #  given each individual feature (as the denominator)
    
      #for each token in the document, calculate the probability of it occurring in a postive
      #  document and in a negative document and add the logs of those to the 
      #  running sums
      #When calculating the probabilities, always add 1 to the numerator of each probability
      #  for add one smoothing (so that we never have a probability of 0). 

      #for debugging, print the overall positive and negative probabilities

      #determine whether positive or negative was more probable (the one with the larger
      #   probability)

      #return a string of "positive" or "negative"
      tokens = self.tokenize(sText)
      postotal = sum(self.dPosFreqs.values())
      negtotal = sum(self.dNegFreqs.values())
      sumlogpos = 0
      sumlogneg = 0
      for word in tokens:
            if self.dPosFreqs.has_key(word):
                  sumlogpos += math.log(float(self.dPosFreqs[word] +1)/postotal)
            else:
                  sumlogpos += math.log(float(1)/postotal)

      for word in tokens:
            if self.dNegFreqs.has_key(word):
                  sumlogneg += math.log(float(self.dNegFreqs[word] + 1)/negtotal)
            else:
                  sumlogneg += math.log(float(1)/negtotal)

      if sumlogpos > sumlogneg:
            return "positive"
      else:
            return "negative"




   def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\'" or c == "_" or c == '-':
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens
