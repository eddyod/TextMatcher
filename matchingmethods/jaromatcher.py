"""
Created on Aug 17, 2019
<<<<<<< HEAD
Uses a Jaro-Winkler distance to compare two strings
=======
JaroMatcher class inherits from AbstractMatcher
>>>>>>> a691046f0a6873868e6c122b90bc6804000b66c9
@author: eodonnell@ucsd.edu
"""

from pyjarowinkler import distance

from .abstract_matcher import AbstractMatcher


class JaroMatcher(AbstractMatcher):
    
    def __init__(self):
        pass
    
    def calculate(self, dataX, dataY):
        """ calculates the jaro distance
        Args:
            dataX: 1st string
            dataY: 2nd string
        Yields:
            float of the jaro distance
        """
        return distance.get_jaro_distance(dataX, dataY)
