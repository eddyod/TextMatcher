"""
Created on Aug 17, 2019
Main class for matching text from a database. 
@author: eodonnell@ucsd.edu
"""

import itertools
import sys
from contextlib import closing

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from connections import MYCONNECTION
from matchfactory import MatchFactory

THRESHOLD = 0.80  # cutoff number



class MatchingStuff:
    """ Main class for matching text strings from a database"""
    
    def __init__(self, factory_method):
        """ sets up the class with the factory method, DB connection and threshold
        Args:
            factory_method: string showing which text matching method to use
        """
        factory = MatchFactory()
        self.matching_method = factory.create_instance(factory_method)
        self._factory_method = factory_method
        self._connection = MYCONNECTION
        self._threshold = THRESHOLD

    def factory_method(self):
        return self._factory_method

    def calculateScoresAndMatch(self, shingle_dict):
        """This iterates through all posssible combinations and if
        the score is above the threshold, add it to a list of lists
        Args:
            shingle_dict: dictionary of primary key and the actual strings to match.
        """
        print('Match data with {} at a threshold of >= {}'.format(self._factory_method, self._threshold))
        cl = len(list(itertools.combinations(shingle_dict, 2)))
        deletes = []
        jaccard_data = []
        count = 1
        for x, y in itertools.combinations(shingle_dict, 2):
            percent = (count / float(cl)) * 100
            sys.stdout.write("Percent done = %0.4f%% Comparing: x:%s with y:%s   \r" % (percent, x, y))
            sys.stdout.flush()
            dataX = shingle_dict[x]
            dataY = shingle_dict[y]
            score = self.matching_method.calculate(dataX, dataY)
            count += 1
            if score > self._threshold:
                deletes.append(y)
                # if x not in deletes:
                jaccard_data.append([x, y, score, dataX, dataY])
        return jaccard_data

    def updateContact(self, dataList):
        """ method to update the contact info. There are a couple of database tables
        to update, so it was completely written out.
        Args:
            dataList: list of primary keys to loop over,
        """
        with closing(self._connection.cursor()) as cursor:
            for row in dataList:
                IDA = row[0]
                IDB = row[1]
                try:
                    sql = 'update agrmnt_sponsor set sponsor_contact_id = {} where sponsor_contact_id = {}'.format(IDA, IDB)
                    print(sql)
                    # cursor.execute(sql)
                    # self.connection.commit()
                except Exception:
                    print("Error updating agrmnt_sponsor.")
                    # self.connection.rollback()
    
                try:
                    sql = 'delete from sponsor_contact where sponsor_contact_id = {}'.format(IDB)
                    cursor.execute(sql)
                    self._connection.commit()
                except Exception:
                    print("Error deleting from sponsor_contact with ID={}".format(IDB))
                    self._connection.rollback()

    def updateSponsor(self, dataList):
        """ method to update the sponsor info. There are a couple of database tables
        to update, so it was completely written out. Also deletes one row per loop
        of the now unnecessary data
        Args:
            dataList: list of primary keys to loop over,
        """
        with closing(self._connection.cursor()) as cursor:
            for row in dataList:
                IDA = row[0]
                IDB = row[1]
                try:
                    sql = 'update sponsor_contact set sponsor_id = {} where sponsor_id = {}'.format(IDA, IDB)
                    print(sql)
                    cursor.execute(sql)
                    self._connection.commit()
                except Exception:
                    print("Error updating sponsor.")
                    self._connection.rollback()

                try:
                    sql = 'update agrmnt_sponsor set sponsor_id = {} where sponsor_id = {}'.format(IDA, IDB)
                    print(sql)
                    cursor.execute(sql)
                    self._connection.commit()
                except Exception:
                    print("Error updating agrmnt_sponsor.")
                    self._connection.rollback()
    
                try:
                    sql = 'delete from sponsor where sponsor_id = {}'.format(IDB)
                    print(sql)
                    cursor.execute(sql)
                    self._connection.commit()
                except Exception:
                    print("Error deleting from sponsor with ID={}".format(IDB))
                    self._connection.rollback()


    def getSponsorData(self, limit):
        """ fetch data, first field has to be the primary key """
        sql = 'select sponsor_id, sponsor_name from sponsor limit {}'.format(limit)
        return self.rowsToDictionary(sql)

    def getSciFiData(self, limit):
        """ fetch data, first field has to be the primary key """
        sql = "select concat(t.abbrv,'.S',e.season,'.E',e.episode_number,' ',trim(e.title)) as x," \
              " replace(synopsis,'\n','') as y" \
              " from episode e inner join tv_show t on e.show_id = t.show_id" \
              " where synopsis is not null and t.show_id = 1 " \
              " order by t.abbrv,e.season,e.episode_number limit {}".format(limit)
                
        return self.rowsToDictionary(sql)

    def rowsToDictionary(self, sql):
        """ take rows for a database query and turn it into a dictionary
        Args:
            sql: string of the actual sql query
        Returns:
            a dictionary of key values
        """
        with closing(self._connection.cursor()) as cursor:
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
            except Exception:
                print("Error selecting data.")
        return {row[0]: ' '.join(row[1:]) for row in rows}

    def createDataframe(self, shingle_dict):
        """Creates a pandas dataframe of score, IDs and the data.
        Iterates over all combinations without repeating combinations.
        Still uses lots of iterations as the number of iterations
        goes up non-linearly. Takes a long time after 5000 rows or so.
        Args:
            shingle_dict: dictionary of data from an sql query
        """
        jaccard_data = self.calculateScoresAndMatch(shingle_dict)
        df = pd.DataFrame(jaccard_data, columns=['x', 'y', 'score', 'dataX', 'dataY'])
        sorted_df = df.sort_values(by=['score'], ascending=False)
        return sorted_df


def heatmap(x_labels, y_labels, values):
    fig, ax = plt.subplots()
    im = ax.imshow(values)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_yticks(np.arange(len(y_labels)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10,
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            text = ax.text(j, i, "%.2f" % values[i, j],
                           ha="center", va="center", color="w", fontsize=6)

    fig.tight_layout()
    plt.show()
