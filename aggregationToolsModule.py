from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

import pandas as pd

# import diffprivlib.models as dp
import numpy as np

import diffprivlib.tools as dp

import pickle	
# datasetFile = "diabetes.csv"



import warnings


# nonprivate_clf = GaussianNB()
# nonprivate_clf.fit(X_train, y_train)

# print("Non-private test accuracy: %.2f%%" % (nonprivate_clf.score(X_test, y_test) * 100))

def getNonPrivateNonZeroCount(array):
	array = np.asanyarray(array)
	if np.issubdtype(array.dtype, np.character):
		array_bool = array != array.dtype.type()
	else:
		array_bool = array.astype(np.bool_, copy=False)
	return sum(array_bool)



def getAggregationReport(dataFileName, accountFile):
	acc = None
	with open(accountFile, "rb") as f:
		acc = pickle.load(f)


	with open(dataFileName, "rb") as f:
		df = pd.read_csv(f)
	columns = df.columns

	aggDict = {}

	for i in columns:
		aggDict[i] = {}
		# with warnings.catch_warnings(record=True) as w:
		# 	warnings.simplefilter("always")
		# 	print(dp.mean(df[columns[1]]))
		# 	print("CAUGHT:", w)
		privateMean = dp.mean(df[i], bounds=(0, 1000), accountant=acc)
		nonPrivateMean = np.mean(df[i])
		aggDict[i]["mean"] = {"private": privateMean, "nonPrivate": nonPrivateMean}
	

	# print("-"*100)

	# for i in columns:
		privateVar = dp.var(df[i], bounds=(0, 1000), accountant=acc)
		nonPrivateVar = np.var(df[i])
		aggDict[i]["var"] = {"private": privateVar, "nonPrivate": nonPrivateVar}
		# print(privateVar, nonPrivateVar)

	# print("-"*100)

	# for i in columns:
		privateStd = dp.std(df[i], bounds=(0, 1000), accountant=acc)
		nonPrivateStd = np.std(df[i])
		aggDict[i]["std"] = {"private": privateStd, "nonPrivate": nonPrivateStd}
		# print(privateStd, nonPrivateStd)


		privateNonZeroCount = dp.count_nonzero(df[i], accountant=acc)
		nonPrivateNonZeroCount = getNonPrivateNonZeroCount(df[i])
		aggDict[i]["nonZero"] = {"private": privateNonZeroCount, "nonPrivate": nonPrivateNonZeroCount}


	return aggDict, acc

if __name__ == "__main__":
	getAggregationReport("UploadedDatasets/diabetes.csv", None)
	