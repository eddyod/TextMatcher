import pyodbc
import itertools
from contextlib import closing
import sys
from fuzzywuzzy import fuzz

import MySQLdb
import re
import math
from collections import Counter
import string
from sklearn.feature_extraction.text import TfidfVectorizer

THRESHOLD = 0.92  # cutoff number
MSCONNECTION = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=ms.domain.edu;'
    r'DATABASE=MyDB;'
    r'UID=imauid'
    r'imapass'
)

MYCONNECTION = MySQLdb.connect("localhost", "imauser", "imapassword", "business_contracts")

re_tok = re.compile('([' + string.punctuation + '“”¨«»®´·º½¾¿¡§£₤‘’])')


def tokenize(text):
    return re_tok.sub(r' \1 ', text.lower()).split()


vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words='english')


def cosineSim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]


WORD = re.compile(r'\w+')


def getCosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text2vector(text):
    words = WORD.findall(text)
    return Counter(words)


def getMeanFuzz(dataX, dataY):
    fuzz_ratio = fuzz.ratio(dataX, dataY)
    fuzz_partial = fuzz.partial_ratio(dataX, dataY)
    token_sort_ratio = fuzz.token_sort_ratio(dataX, dataY)
    return ( (fuzz_ratio + fuzz_partial + token_sort_ratio) / float(3.0) ) / 100


def calculateScoresAndMatch(shingle_dict):
    print("List of data with match >= ", THRESHOLD)
    cl = len(list(itertools.combinations(shingle_dict, 2)))
    deletes = []
    jaccard_data = []
    count = 1
    for x, y in itertools.combinations(shingle_dict, 2):
        percent = (count / float(cl)) * 100
        sys.stdout.write("Percent done = %0.4f%% Comparing: x:%d with y:%d   \r" % (percent, x, y))
        sys.stdout.flush()
        dataX = shingle_dict[x]
        dataY = shingle_dict[y]
        score = getMeanFuzz(dataX, dataY)
        count += 1
        if score > THRESHOLD:
            deletes.append(y)
            if x not in deletes:
                jaccard_data.append([x, y, score, dataX, dataY])
    return jaccard_data


def sortAndPrint(jaccard_data, outputFile):
    print('\nSorting data into {}'.format(outputFile))
    sorted_list = sorted(jaccard_data, key=lambda x: x[2], reverse=True)
    f = open(outputFile, "w")
    count = 1
    f.write("Score\t")
    f.write("ID - A\t")
    f.write("Match A\t")
    f.write("ID - B\t")
    f.write("Match B\n")
    for row in sorted_list:
        x = row[0]
        y = row[1]
        score = row[2]
        dataX = row[3]
        dataY = row[4]
        f.write("{0:.2f}".format(round(score, 4)))
        f.write("\t")
        f.write(str(x).ljust(5))
        f.write("\t")
        f.write(str(dataX))
        f.write("\t")
        f.write(str(y).ljust(5))
        f.write("\t")
        f.write(str(dataY))
        f.write("\n")
        count += 1



def updateContact(dataList):
    with closing(MYCONNECTION.cursor()) as cursor:
        for row in dataList:
            IDA = row[0]
            IDB = row[1]
            try:
                sql = 'update agrmnt_sponsor set sponsor_contact_id = {} where sponsor_contact_id = {}'.format(IDA, IDB)
                print(sql)
                # cursor.execute(sql)
                # MYCONNECTION.commit()
            except Exception:
                print("Error updating agrmnt_sponsor.")
                # MYCONNECTION.rollback()

            try:
                sql = 'delete from sponsor_contact where sponsor_contact_id = {}'.format(IDB)
                cursor.execute(sql)
                MYCONNECTION.commit()
            except Exception:
                print("Error deleting from sponsor_contact with ID={}".format(IDB))
                MYCONNECTION.rollback()


def updateSponsor(dataList):
    with closing(MYCONNECTION.cursor()) as cursor:
        for row in dataList:
            IDA = row[0]
            IDB = row[1]
            try:
                sql = 'update sponsor_contact set sponsor_id = {} where sponsor_id = {}'.format(IDA, IDB)
                print(sql)
                cursor.execute(sql)
                MYCONNECTION.commit()
            except Exception:
                print("Error updating sponsor.")
                MYCONNECTION.rollback()

            try:
                sql = 'update agrmnt_sponsor set sponsor_id = {} where sponsor_id = {}'.format(IDA, IDB)
                print(sql)
                cursor.execute(sql)
                MYCONNECTION.commit()
            except Exception:
                print("Error updating agrmnt_sponsor.")
                MYCONNECTION.rollback()

            try:
                sql = 'delete from sponsor where sponsor_id = {}'.format(IDB)
                print(sql)
                cursor.execute(sql)
                MYCONNECTION.commit()
            except Exception:
                print("Error deleting from sponsor with ID={}".format(IDB))
                MYCONNECTION.rollback()


def getExternalOrgData():
    """ fetch data, first field has to be the primary key """
    sql = """select eo.Id, eo.ExternalOrg, c.address1, c.address2, c.ContactName
    from ExternalOrg eo
    INNER JOIN Contact c on eo.Id = c.ExternalOrgId
    WHERE eo.Id NOT IN (666666666)
    AND
    (
    c.address1 is not null or c.address2 is not null
    OR LEN(c.ContactName) > 4
    )
    order by eo.ExternalOrg, c.address1, c.ContactName"""
    return rowsToDictionary(MSCONNECTION, sql)


def getContactData(limit):
    """ fetch data, first field has to be the primary key """
    sql = """select
        sc.sponsor_contact_id,
        (CASE WHEN s.sponsor_name is null or s.sponsor_name = '' THEN 'NA ' ELSE s.sponsor_name END) as sponsor_name,
        (CASE WHEN sc.contact_name is null or sc.contact_name = '' THEN 'NA' ELSE sc.contact_name END) as contact,
        (CASE WHEN sc.address1 is null or sc.address1 = '' THEN 'NA' ELSE sc.address1 END) as address1,
        (CASE WHEN sc.address2 is null or sc.address2 = '' THEN 'NA' ELSE sc.address2 END) as address2,
        (CASE WHEN sc.city is null or sc.city = '' THEN 'NA' ELSE sc.city END) as city,
        (CASE WHEN sc.zip is null or sc.zip = '' THEN 'NA' ELSE sc.zip END) as zip,
        (CASE WHEN sc.state is null or sc.state = '' THEN 'NA' ELSE sc.state END) as state,
        (CASE WHEN sc.email is null or sc.email = '' THEN 'NA' ELSE sc.email END) as email
        from sponsor s
        inner join sponsor_contact sc on s.sponsor_id = sc.sponsor_id
        where (sc.contact_name is not null or sc.address1 is not null or sc.email is not null)
        order by s.sponsor_name, sc.email, sc.contact_name
        limit """ + str(limit)
    return rowsToDictionary(MYCONNECTION, sql)


def getSponsorData(limit):
    """ fetch data, first field has to be the primary key """
    sql = 'select sponsor_id, sponsor_name from sponsor limit {}'.format(limit)
    return rowsToDictionary(MYCONNECTION, sql)


def rowsToDictionary(connection, sql):
    with closing(connection.cursor()) as cursor:
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
        except Exception:
            print("Error selecting data.")
    return {row[0]: ' '.join(row[1:]) for row in rows}
