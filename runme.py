'''
Created on Aug 17, 2019
Main program to run.
Currently there are 4 factories to use. The default is fuzzywuzzy. It
has good results and is very fast.
1. FuzzyMatcher
2. CosineMatcher
3. NltkMatcher
4. TfidfMatcher
@author: eodonnell@ucsd.edu
'''
from matchingStuff import MatchingStuff
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


matcher = MatchingStuff('FuzzyMatcher')

data_dict = matcher.getSponsorData(10000)
#print(data_dict)
df = matcher.createDataframe(data_dict)
print(df.head(25))
df.to_csv("sponsors.csv", index = False)

"""
heatmap1_data = pd.pivot_table(df, values='score', 
                     index=['x'], 
                     columns='y')

hm = sns.heatmap(heatmap1_data, cmap="YlGnBu")
plt.show()
"""
#matched_data = matcher.calculateScoresAndMatch(data_dict)
#matcher.sortAndPrint(matched_data, 'sponsors.txt')