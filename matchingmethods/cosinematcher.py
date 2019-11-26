"""
Created on Aug 17, 2019
Uses a basic cosine similarty to compare two strings
Converts the strings to vectors, takes the intersection, 
then computes the cosine similarity
@author: eodonnell@ucsd.edu
"""

import math
import re
from collections import Counter

from .abstract_matcher import AbstractMatcher

WORD = re.compile(r'\w+')


class CosineMatcher(AbstractMatcher):
    
    def __init__(self):
        pass
    
    def calculate(self, dataX, dataY):
        """ calculates the cosine similarity
        Args:
            dataX: 1st string
            dataY: 2nd string
        Yields:
            float of the cosine similarity
        """
        vec1 = self.text_to_vector(dataX)
        vec2 = self.text_to_vector(dataY)
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator


    @staticmethod
    def text_to_vector(text):
        words = WORD.findall(text)
        return Counter(words)
