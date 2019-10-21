"""
Created on Aug 17, 2019
FuzzyMatcher class inherits from AbstractMatcher
Uses the fuzzywuzzy library, which is very fast
@author: eodonnell@ucsd.edu
"""

from fuzzywuzzy import fuzz

from .abstract_matcher import AbstractMatcher


class FuzzyMatcher(AbstractMatcher):

    def calculate(self, dataX, dataY):
        """ calculates two different fuzzy matches, then averages them
        Args:
            dataX: 1st string
            dataY: 2nd string
        Yields:
            a float of the average of the two ratios
        """
        fuzz_ratio = fuzz.ratio(dataX, dataY)
        token_sort_ratio = fuzz.token_sort_ratio(dataX, dataY)
        return ((fuzz_ratio + token_sort_ratio) / float(2.0)) / 100
