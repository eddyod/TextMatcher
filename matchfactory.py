'''
Created on Aug 17, 2019

@author: eodonnell@ucsd.edu
'''
from inspect import getmembers, isclass, isabstract
import matchingmethods


class MatchFactory(object):
    '''
    classdocs
    '''
    matchingmethods = {}


    def __init__(self):
        '''
        Constructor
        '''
        self.load_matchingmethods()
        
        
    def load_matchingmethods(self):
        classes = getmembers(matchingmethods, lambda m: isclass(m) and not isabstract(m))
        
        for name, _type in classes:
            if isclass(_type) and issubclass(_type, matchingmethods.AbstractMatcher):
                self.matchingmethods.update([[name, _type]])
                
    def create_instance(self, matchname):
        if matchname in self.matchingmethods:
            return self.matchingmethods[matchname]()
        else:
            return self.matchingmethods.NullMethod(matchname)