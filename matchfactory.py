"""
Created on Aug 17, 2019

@author: eodonnell@ucsd.edu
"""
from inspect import getmembers, isclass, isabstract
from typing import Dict, Any

import matchingmethods


class MatchFactory(object):
    """
    classdocs
    """
    matchermethods: Dict[Any, Any] = {}

    def __init__(self):
        """
        Constructor
        """
        self.load_matchingmethods()
        
    def load_matchingmethods(self):
        classes = getmembers(matchingmethods, lambda m: isclass(m) and not isabstract(m))
        
        for name, _type in classes:
            if isclass(_type) and issubclass(_type, matchingmethods.AbstractMatcher):
                self.matchermethods.update([[name, _type]])
                
    def create_instance(self, matchname):
        if matchname in self.matchermethods:
            return self.matchermethods[matchname]()
        else:
            return matchingmethods.NullMethod(matchname)
