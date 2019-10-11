import MySQLdb
import re
import time
import math
from collections import Counter
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import itertools
# python -m spacy download en_core_web_lg
# nltk.download('punkt') # if necessary...


stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]


'''remove punctuation, lowercase, stem'''


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


re_tok = re.compile('([' + string.punctuation + '“”¨«»®´·º½¾¿¡§£₤‘’])')


def tokenize(text):
    return re_tok.sub(r' \1 ', text.lower()).split()


vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words='english')


def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]


CONNECTION = MySQLdb.connect("asdfasdf", "asdfasd", "sdfasdf", "business_contracts")
CURSOR = CONNECTION.cursor()


GETDATA = """select sponsor_id as id, sponsor_name from sponsor order by sponsor_name"""


def insert_record(x, y, score):
    ADDMATCH = """insert into matching
    (episode_x_id, episode_y_id, score) values (%s, %s, %s)"""
    try:
        CURSOR.execute(ADDMATCH, [x, y, score])
        CONNECTION.commit()
    except:
        print("Something went wrong with the insert.")
        CONNECTION.rollback()


WORD = re.compile(r'\w+')


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def main():

    sponsors = {}
    CURSOR.execute(GETDATA)
    rows = CURSOR.fetchall()
    sponsors = dict((row[0], row[1]) for row in rows)

    print('Number of sponsors:', len(sponsors))
    start_time = time.time()
    counter = 1
    for x, y in itertools.combinations(sponsors, 2):
        v1 = sponsors[x]
        v2 = sponsors[y]
        vector1 = text_to_vector(v1)
        vector2 = text_to_vector(v2)
        score1 = get_cosine(vector1, vector2)
        score2 = cosine_sim(v1, v2)
        score1 = "%10.5f" % score1
        score2 = "%10.5f" % score2
        print(x, y, score1, score2)
        counter += 1
    print(counter, "computations with Combo method --- %s seconds ---" %
          (time.time() - start_time))


if __name__ == '__main__':
    main()
