'''
Created on Aug 17, 2019
Main program to run.
Currently there are 4 factories to use. The default is fuzzywuzzy. It
has good results and is very fast.
1. FuzzyMatcher
2. CosineMatcher
3. NltkMatcher
4. TfidfMatcher
@author: eodonnell@ucsd.edu
'''

from matchingStuff import MatchingStuff

matcher = MatchingStuff('FuzzyMatcher')

data_dict = matcher.getSponsorData(500)
matched_data = matcher.calculateScoresAndMatch(data_dict)
matcher.sortAndPrint(matched_data, 'sponsors.txt')