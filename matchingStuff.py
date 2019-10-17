'''
Created on Aug 17, 2019
Main class for matching text from a database. 
@author: eodonnell@ucsd.edu
'''

import itertools
from contextlib import closing
import sys
from matchfactory import MatchFactory

import MySQLdb

THRESHOLD = 0.72  # cutoff number
MYCONNECTION = MySQLdb.connect("localhost", "user", "pass", "db")


class MatchingStuff:
    """ Main class for matching text strings from a database"""
    
    def __init__(self, factory_method):
        """ sets up the class with the factory method, DB connection and threshold
        Args:
            factory_method: string showing which text matching method to use
        """
        factory = MatchFactory()
        self.matching_method = factory.create_instance(factory_method)
        self.factory_method = factory_method
        self.connection = MYCONNECTION
        self.threshold = THRESHOLD
        

    def calculateScoresAndMatch(self, shingle_dict):
        """This iterates through all posssible combinations and if
        the score is above the threshold, add it to a list of lists
        Args:
            shingle_dict: dictionary of primary key and the actual strings to match.
        """
        print('Match data with {} at a threshold of >= {}'.format(self.factory_method, self.threshold))
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
            score = self.matching_method.calculate(dataX, dataY)
            count += 1
            if score > self.threshold:
                deletes.append(y)
                if x not in deletes:
                    jaccard_data.append([x, y, score, dataX, dataY])
        return jaccard_data


    def sortAndPrint(self, jaccard_data, outputFile):
        """ Takes in a list of lists, sorts it, then writes
        it to a nice output file for viewing
        Args:
            jaccard_data: list of lists to be sorted and outputted
            outputFile: name of file to write to
        """
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



    def updateContact(self, dataList):
        """ method to update the contact info. There are a couple of database tables
        to update, so it was completely written out.
        Args:
            dataList: list of primary keys to loop over,
        """ 
        with closing(self.connection.cursor()) as cursor:
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
                    self.connection.commit()
                except Exception:
                    print("Error deleting from sponsor_contact with ID={}".format(IDB))
                    self.connection.rollback()


    def updateSponsor(self, dataList):
        """ method to update the sponsor info. There are a couple of database tables
        to update, so it was completely written out. Also deletes one row per loop
        of the now unnecessary data
        Args:
            dataList: list of primary keys to loop over,
        """ 
        with closing(self.connection.cursor()) as cursor:
            for row in dataList:
                IDA = row[0]
                IDB = row[1]
                try:
                    sql = 'update sponsor_contact set sponsor_id = {} where sponsor_id = {}'.format(IDA, IDB)
                    print(sql)
                    cursor.execute(sql)
                    self.connection.commit()
                except Exception:
                    print("Error updating sponsor.")
                    self.connection.rollback()

                try:
                    sql = 'update agrmnt_sponsor set sponsor_id = {} where sponsor_id = {}'.format(IDA, IDB)
                    print(sql)
                    cursor.execute(sql)
                    self.connection.commit()
                except Exception:
                    print("Error updating agrmnt_sponsor.")
                    self.connection.rollback()
    
                try:
                    sql = 'delete from sponsor where sponsor_id = {}'.format(IDB)
                    print(sql)
                    cursor.execute(sql)
                    self.connection.commit()
                except Exception:
                    print("Error deleting from sponsor with ID={}".format(IDB))
                    self.connection.rollback()


    def getSponsorData(self, limit):
        """ fetch data, first field has to be the primary key """
        sql = 'select sponsor_id, sponsor_name from sponsor limit {}'.format(limit)
        return self.rowsToDictionary(sql)


    def rowsToDictionary(self, sql):
        """ take rows for a database query and turn it into a dictionary
        Args:
            sql: string of the actual sql query
        """
        with closing(self.connection.cursor()) as cursor:
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
            except Exception:
                print("Error selecting data.")
        return {row[0]: ' '.join(row[1:]) for row in rows}
