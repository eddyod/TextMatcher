from .abstract_matcher import AbstractMatcher


class NullMethod(AbstractMatcher):

    def __init__(self, methodname):
        self._methodname = methodname
        print('Unknown method "%s".' % methodname)

    def calculate(self):
        pass
