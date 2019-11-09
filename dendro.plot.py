import re

import nltk
import pandas as pd
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english", ignore_stopwords=False)
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram


def normalize(X):
    normalized = []
    for x in X:
        words = nltk.word_tokenize(x)
        normalized.append(' '.join([stemmer.stem(word) for word in words if re.match('[a-zA-Z]+', word)]))
    return normalized


df = pd.read_csv('/home/eodonnell/git/design.patterns/datafiles/episodes.csv')
pipe = Pipeline([
    ('normalize', FunctionTransformer(normalize, validate=False)),
    ('counter_vectorizer', CountVectorizer(
        stop_words='english',
        ngram_range=(1, 3)
    )),
    ('tfidf_transform', TfidfTransformer())])

tfidf_matrix = pipe.fit_transform([x for x in df['synopsis']])
similarity_distance = 1 - cosine_similarity(tfidf_matrix)

mergings = linkage(similarity_distance, method='complete')
dendrogram_ = dendrogram(mergings,
                         labels=[x for x in df["title"]],
                         leaf_rotation=45,
                         leaf_font_size=12,
                         )

fig = plt.gcf()
_ = [lbl.set_color('r') for lbl in plt.gca().get_xmajorticklabels()]
fig.set_size_inches(108, 21)

plt.show()
