"""
Created on Aug 17, 2019
Concrete class to create an NLTK factory for text matching
@author: eodonnell@ucsd.edu
"""

import string

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

from .abstract_matcher import AbstractMatcher


class NltkMatcher(AbstractMatcher):
    """ Concrete class that inherits the abstract matcher class.
        This uses the sklean library for feature extraction.
        Just one method with some helper methods
    """
    
    def __init__(self):
        pass
    
    def calculate(self, dataX, dataY):
        """ calculates the cosine similarity between two
        strings. It uses  tfidf  vectorizer from sklearn
        Args:
            dataX: first string
            dataY: 2nd string
        Yields:
            float: the actual cosine similarity value
        """
        tfidf = vectorizer.fit_transform([dataX, dataY])
        return ((tfidf * tfidf.T).A)[0, 1]


stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]


"""remove punctuation, lowercase, stem"""


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
