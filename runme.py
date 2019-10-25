"""
Created on Aug 17, 2019
Main program to run.
Currently there are 4 factories to use. The default is fuzzywuzzy. It
has good results and is very fast.
1. FuzzyMatcher
2. CosineMatcher
3. NltkMatcher
4. TfidfMatcher
5. JaroMatcher
@author: eodonnell@ucsd.edu
"""
from pprint import pprint as pp

from matchingStuff import MatchingStuff

matcher = MatchingStuff('FuzzyMatcher')

data_dict = matcher.getSponsorData(5000)
#print(data_dict)
# df = pd.DataFrame.from_dict(data_dict, columns=['title', 'synopsis'], orient = 'index')
# df = pd.DataFrame(list(data_dict.items()), columns=['title', 'synopsis'])
df = matcher.createDataframe(data_dict)
# print(df[['score', 'x', 'y', 'dataX']].head(25))
pp(df.head(50))

# df = df[['score', 'x', 'y', 'dataX']]
# df['dataX'] = df['dataX'].str[:50]
# df['dataY'] = df['dataY'].str[:50]
df.to_csv("sponsors.csv", index=False)
"""
heatmap1_data = pd.pivot_table(df, values='score', 
                     index=['x'], 
                     columns='y')

hm = sns.heatmap(heatmap1_data, cmap="YlGnBu")
plt.show()
"""
