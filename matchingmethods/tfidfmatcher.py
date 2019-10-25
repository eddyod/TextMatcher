from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction import text

from .abstract_matcher import AbstractMatcher

stemmer = SnowballStemmer("english", ignore_stopwords=False)
import nltk
import re


class TfidfMatcher(AbstractMatcher):

    def __init__(self):
        pass

    def calculate(self, dataX, dataY):
        # tfidf = vectorizer.fit_transform([dataX, dataY])
        # my_stop_words = text.ENGLISH_STOP_WORDS.union(["Inc", "Hospital"])
        pipe = Pipeline([
            ('normalize', FunctionTransformer(self.normalize, validate=False)),
            ('counter_vectorizer', CountVectorizer(
                stop_words = 'english',
                ngram_range = (1, 2)
            )),
            ('tfidf_transform', TfidfTransformer())
        ])

        tfidf = pipe.fit_transform([dataX, dataY])
        # similarity_distance = 1 - cosine_similarity(tfidf_matrix)
        result = ((tfidf * tfidf.T).A)[0, 1]
        return result

    @staticmethod
    def normalize(X):
        normalized = []
        for x in X:
            words = nltk.word_tokenize(x)
            normalized.append(' '.join([stemmer.stem(word) for word in words if re.match('[a-zA-Z]+', word)]))
        return normalized
