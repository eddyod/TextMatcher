from .abstract_matcher import AbstractMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import re

class TfdifMatcher(AbstractMatcher):
    
    def __init__(self):
        pass
    
    def calculate(self, dataX, dataY):
        tfidf = vectorizer.fit_transform([dataX, dataY])
        return ((tfidf * tfidf.T).A)[0, 1]
 
 
# vectorizer = TfidfVectorizer()

re_tok = re.compile('([' + string.punctuation + '“”¨«»®´·º½¾¿¡§£₤‘’])')

def tokenize(text):
    return re_tok.sub(r' \1 ', text.lower()).split()

vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words='english')