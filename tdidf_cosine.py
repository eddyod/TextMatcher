import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords 
from string import punctuation
from nltk.collocations import *
import MySQLdb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
from nltk.probability import FreqDist
from collections import defaultdict
from heapq import nlargest
import nltk, string 
from sklearn.neighbors import KNeighborsClassifier
import numpy as np


CONNECTION = MySQLdb.connect("localhost", "sdfsdf", "sdfasdf", "sdfsdf")
CURSOR = CONNECTION.cursor()
GETDATA = """select episode_id, synopsis from episode
    where synopsis is not null
    order by episode_id limit 5"""
CURSOR.execute(GETDATA)
rows = CURSOR.fetchall()
episodes = {}
for row in rows:
    id = int(row[0])
    text = row[1]
    text = text.strip()
    episodes[id] = text

GETDATA = """select episode_id, trim(synopsis) from episode where synopsis is not null
            order by episode_id"""

            
def insert_record(x, y, score):
    ADDMATCH = """insert into matching 
    (episode_x_id, episode_y_id, score) values (%s, %s, %s)"""
    try:
        CURSOR.execute(ADDMATCH, [x, y, score])
        CONNECTION.commit()
    except:
        print("Something went wrong:")
        CONNECTION.rollback()

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

for episode_x_id, value in episodes.items():
    for episode_y_id, v2 in episodes.items():
        score = cosine_sim(episodes[episode_x_id], episodes[episode_y_id])
        #score = round(score,5)
        #insert_record(episode_x_id, episode_y_id, score) 
        score = "%10.5f" % score
        print(episode_x_id, episode_y_id, score)

