from .abstract_matcher import AbstractMatcher

class NullMethod(AbstractMatcher):
    def __init__(self, methodname):
        self._methodname = methodname

    def calculate(self):
        print('Unknown method "%s".' % self._methodname)
