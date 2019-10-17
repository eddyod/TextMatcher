'''
Created on Aug 17, 2019
Abstract class that is used by the other matching factories
@author: eodonnell@ucsd.edu
'''

import abc


class AbstractMatcher(metaclass=abc.ABCMeta):
    """ initial abstract class"""
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


    @abc.abstractmethod
    def calculate(self):
        pass
