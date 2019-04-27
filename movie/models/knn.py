# KNN Model

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

X_all_df = df.drop(['rating','title'], axis=1)        # everything except the 'label' column
y_all_df = df[ 'rating' ]

print("+++ start of numpy/scikit-learn +++")

X_all = X_all_df.values        # iloc == "integer locations" of rows/cols
y_all = y_all_df.values

indices = np.random.permutation(len(y_all)) 
x_labeled = X_all[indices]
y_labeled = y_all[indices]

TEST_SIZE = 30251
x_test = x_labeled[:TEST_SIZE]
y_test = y_labeled[:TEST_SIZE]

x_train = x_labeled[TEST_SIZE:]
y_train = y_labeled[TEST_SIZE:]

from sklearn.neighbors import KNeighborsRegressor

best_score = 0
best_k = 0
for k in [1,3,5,7,9,11,15,21,32,42,51,71,91]:
  knn = KNeighborsRegressor(n_neighbors=k)
  cv_scores = cross_val_score( knn, x_train, y_train, cv=5 )
  av = cv_scores.mean()
  print(k , 'neighbors has average: ', av)
  if av > best_score:
      best_score = av
      best_k = k
print("best k is", best_k)

knn_train = KNeighborsRegressor(n_neighbors=best_k) 
knn_train.fit(x_train, y_train) 
print("\nCreated and trained a knn classifier with k =", best_k)

# Now, run our test set!
print("For the input data in X_test,")
print("The predicted outputs are")
predicted_labels = knn_train.predict(x_test)
print(predicted_labels[:10])

print("and the actual labels are")
actual_labels = y_test
print(actual_labels[:10])

# accuracy
from sklearn.metrics import mean_squared_error

# squared_errors = []
# for p in predicted_labels:
#     for a in actual_labels:
#         squared_errors.append((a-p)**2)
# ase = sum(squared_errors)/len(squared_errors)
variance = np.var(actual_labels)

mse = mean_squared_error(actual_labels, predicted_labels)

print("The MSE of the KNN model is:", mse)
r_squared = 1-(mse/variance)
print("The R-squared is:", r_squared)