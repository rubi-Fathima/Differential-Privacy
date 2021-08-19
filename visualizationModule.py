from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

import pandas as pd

# import diffprivlib.models as dp
import numpy as np

import diffprivlib.tools as dp

import pickle	
# datasetFile = "diabetes.csv"



# nonprivate_clf = GaussianNB()
# nonprivate_clf.fit(X_train, y_train)

# print("Non-private test accuracy: %.2f%%" % (nonprivate_clf.score(X_test, y_test) * 100))


def getVisualization(dataFileName, accountFile):
	acc = None
	with open(accountFile, "rb") as f:
		acc = pickle.load(f)
	vizDict = {}
	with open(dataFileName, "rb") as f:
		df = pd.read_csv(f)
	columns = df.columns
	print(columns)
	for i in columns:
		privateHist = dp.histogram(df[i], accountant=acc)
		nonPrivateHist = np.histogram(df[i])
		privateValues, privateLabels = list(map(float, privateHist[0])), list(map(int, privateHist[1]))
		nonPrivateValues, nonPrivateLabels = list(map(float, nonPrivateHist[0])), list(map(int, nonPrivateHist[1]))
		vizDict[i] = {"private":{"labels": privateLabels, "values": privateValues},
						"nonPrivate": {"labels": nonPrivateLabels, "values": nonPrivateValues}}
	return vizDict, acc




if __name__ == "__main__":
	getVisualizations("UploadedDatasets/diabetes.csv")
	