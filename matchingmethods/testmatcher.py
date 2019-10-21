import re
import string

from sklearn.feature_extraction.text import TfidfVectorizer

from .abstract_matcher import AbstractMatcher


class TestMatcher(AbstractMatcher):

    def __init__(self):
        pass

    def calculate(self, dataX, dataY):
        tfidf = vectorizer.fit_transform([dataX, dataY])
        result = ((tfidf * tfidf.T).A)[0, 1]
        # print(result)
        return result


# vectorizer = TfidfVectorizer()

re_tok = re.compile('([' + string.punctuation + '“”¨«»®´·º½¾¿¡§£₤‘’])')

def tokenize(text):
    return re_tok.sub(r' \1 ', text.lower()).split()


vectorizerX = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
vectorizer = TfidfVectorizer(tokenizer=tokenize, max_features=200000, stop_words='english', ngram_range=(1, 3))
vectorizer1 = TfidfVectorizer(tokenizer=tokenize, max_features=200000, min_df=0.2, stop_words='english',
                              ngram_range=(1, 3))
