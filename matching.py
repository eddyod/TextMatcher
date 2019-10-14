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

print(__name__)


class Matching:
    """Base class for setting up the matching rows.

    Attributes:
        :connection: setup the database connection
        :sql: Query to fetch data. Primary key first and then all other fields
    """

    def __init__(self, connection, sql):
        """The constructor of the Matching class."""
        self.connection = connection
        self.sql = sql
