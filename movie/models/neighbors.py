# KNN Model - clustering (neighbors)

import numpy as np
from sklearn import datasets
import pandas as pd

try: # different imports for different versions of scikit-learn
    from sklearn.model_selection import cross_val_score   # simpler cv this week
except ImportError:
    try:
        from sklearn.cross_validation import cross_val_score
    except:
        print("No cross_val_score!")

df = pd.read_csv('../../data/movies_ratings.csv', header=0)
df.head()
df.info()

print("+++ End of pandas +++\n")

all_orig = df
all_df = df.drop(['title', 'movieId', 'userId'], axis=1)        # everything except the 'label' column

print("+++ start of numpy/scikit-learn +++")

all_orig = all_orig.values
all_data = all_df.values        # iloc == "integer locations" of rows/cols
# print(type(all_data))


# TEST_SIZE = 30251
# x_test = x_labeled[:TEST_SIZE]
# y_test = y_labeled[:TEST_SIZE]

# x_train = x_labeled[TEST_SIZE:]
# y_train = y_labeled[TEST_SIZE:]

from sklearn.neighbors import NearestNeighbors

nbrs = NearestNeighbors(n_neighbors=5) 
nbrs.fit(all_data)

print("sample:",[all_orig[0]])
 
distances, indices = nbrs.kneighbors([all_data[0]])

for i in indices:
    print(all_orig[i])
