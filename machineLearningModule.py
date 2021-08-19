from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


import pandas as pd

import diffprivlib.models as dp
import numpy as np

import pickle

from random import shuffle
from io import StringIO
# datasetFile = "diabetes.csv"



# nonprivate_clf = GaussianNB()
# nonprivate_clf.fit(X_train, y_train)
# print("Non-private test accuracy: %.2f%%" % (nonprivate_clf.score(X_test, y_test) * 100))

def shuffleData(df):
	newDfColumns = []
	for i in df.columns:
		columnDf = df[i]
		columnDfRandom = columnDf.copy()
		shuffle(columnDfRandom)
		newDfColumns.append(columnDfRandom)
	newDf = pd.concat(newDfColumns, axis=1)
	return newDf



def getFileInfo(dataFilename):
	with open(dataFilename, "rb") as f:
		df = pd.read_csv(f)
	print(df.head())
	sampleDf = df.head()
	sampleDf = shuffleData(sampleDf)
	# sampleDf.reset_index(drop=True, inplace=True)
	return {"table": sampleDf.to_html(classes="table table-bordered table-hover"), "columnNames": list(sampleDf.columns)}
	# return sampleDf.to_dict()



def getResults(dataFileName, yColumnName, modelName, accountFile):
	print("GOT MODEL:", modelName)
	acc = None
	with open(accountFile, "rb") as f:
		acc = pickle.load(f)
	with open(dataFileName, "rb") as f:
		df = pd.read_csv(f)


	df = df.fillna(0)
	X = df.loc[:, df.columns!=yColumnName].to_numpy()
	y = df[yColumnName].to_numpy()
	X_train, X_test, y_train, y_test = train_test_split(X, y)


	nonprivate_clf = None
	df_clf = None
	inf_dp_clf = None



	if modelName == "gaussianNB":
		nonprivate_clf = GaussianNB()
		dp_clf = dp.GaussianNB(accountant=acc)
		inf_dp_clf = dp.GaussianNB(epsilon=float("inf"))
		scoreType = "Accuracy"

	elif modelName == "logisticReg":
		nonprivate_clf = LogisticRegression()
		dp_clf = dp.LogisticRegression(accountant=acc)
		inf_dp_clf = dp.LogisticRegression(epsilon=float("inf"))
		scoreType = "Accuracy"

	elif modelName == "linearReg":
		nonprivate_clf = LinearRegression()
		dp_clf = dp.LinearRegression(accountant=acc)
		inf_dp_clf = dp.LinearRegression(epsilon=float("inf"))
		scoreType = "R2 Score"


	nonprivate_clf.fit(X_train, y_train)
	nonPrivateTestScore = nonprivate_clf.score(X_test, y_test)
	if scoreType == "Accuracy":
		nonPrivateTestScore *= 100


	dp_clf.fit(X_train, y_train)
	dpTestScore = dp_clf.score(X_test, y_test)
	if scoreType == "Accuracy":
		dpTestScore *= 100
	agreement = dp_clf.score(X_test, nonprivate_clf.predict(X_test)) * 100

	inf_dp_clf.fit(X_train, y_train)
	infDpTestScore = inf_dp_clf.score(X_test, y_test)
	if scoreType == "Accuracy":
		infDpTestScore *= 100
	infAgreement = inf_dp_clf.score(X_test, nonprivate_clf.predict(X_test)) * 100


	epsilons = np.logspace(-2, 2, 50)
	# bounds = ([4.3, 2.0, 1.1, 0.1], [7.9, 4.4, 6.9, 2.5])
	accuracy = list()
	for epsilon in epsilons:
		if modelName == "gaussianNB":
			clf = dp.GaussianNB(epsilon=epsilon, accountant=acc)
		elif modelName == "logisticReg":
			clf = dp.LogisticRegression(epsilon=epsilon, accountant=acc)
		elif modelName == "linearReg":
			clf = dp.LinearRegression(epsilon=epsilon+1, accountant=acc)
		clf.fit(X_train, y_train)
		accuracy.append(clf.score(X_test, y_test))

	resultDict = {"nonPrivate": round(nonPrivateTestScore, 2),
				"private": round(dpTestScore, 2),
				"infinitePrivate": round(infDpTestScore),
				"agreement": round(agreement, 2),
				"infiniteAgreement": round(infAgreement, 2),
				"scoreType": scoreType,
				"labels": list(map(lambda x: round(x, 2), epsilons)),
				"values": accuracy,
				"xLabel": "Epsilons",
				"yLabel": scoreType
			}
	return resultDict, acc




def cleanFile(cleanDict):
	datasetFilename = cleanDict["datasetFilename"]
	with open(datasetFilename, "rb") as f:
		df = pd.read_csv(f)
	print("BEFORE:")
	print(df)
	for i in cleanDict:
		if "editColumn" in i:
			columnToRemove = i.split("---")[1]
			# del df[columnToRemove]
			df.drop([columnToRemove], axis=1, inplace=True)
	print("AFTER DELETION:")
	print(df)
	print("SAVED AT:", datasetFilename)
	df.to_csv(datasetFilename, index=False)
	print(df)





if __name__ == "__main__":
	# with open(dataFileName, "rb") as f:
	# 	df = pd.read_csv(f)

	from sklearn.model_selection import train_test_split
	# from sklearn import datasets

	# dataset = datasets.load_diabetes()
	# with open("Classification Datasets\\creditcardSample.csv", "wb") as f:
	df = pd.read_csv("Classification Datasets\\creditcardSample.csv")
	for i in df.columns:
		print(df[i].dtype)
	# print(df.isnull().any())
	df = df.fillna(0)
	# X_train, X_test, y_train, y_test = train_test_split(dataset.data[:, :2], dataset.target, test_size=0.2)
	# print("Train examples: %d, Test examples: %d" % (X_train.shape[0], X_test.shape[0]))
	yColumnName = "Class"
	X = df.loc[:, df.columns!=yColumnName].to_numpy()
	y = df[yColumnName].to_numpy()
	X_train, X_test, y_train, y_test = train_test_split(X, y)
	print(X_train)
	print(y_train)


	# from sklearn.linear_model import LinearRegression as sk_LinearRegression

	# regr = sk_LinearRegression()
	regr = LogisticRegression()
	regr.fit(X_train, y_train)
	baseline = regr.score(X_test, y_test)
	print("Non-private baseline R2 score: %.2f" % baseline)


	# from diffprivlib.models import LinearRegression

	# regr = LinearRegression()
	# regr.fit(X_train, y_train)

	# print("R2 score for epsilon=%.2f: %.2f" % (regr.epsilon, regr.score(X_test, y_test)))


	# from sklearn import datasets
	# import pandas as pd 

	# data = datasets.load_diabetes()
	# print(data)

	# df = pd.DataFrame(data=data['data'], columns = data['feature_names'])

	# df['Y'] = data['target']

	# df.to_csv('diabetesRegression.csv', sep = ',', index = False)










	# from sklearn import datasets
	# dataset = datasets.load_diabetes()

	# print(dataset["data"])
	# pd.DataFrame(dataset["data"]).to_csv("diabetesRegression.csv")

	# X_train, X_test, y_train, y_test = train_test_split(dataset.data[:, :2], dataset.target, test_size=0.2)
	# print("Train examples: %d, Test examples: %d" % (X_train.shape[0], X_test.shape[0]))




	# nonprivate_clf = None
	# df_clf = None
	# inf_dp_clf = None

	# nonprivate_clf = LinearRegression()
	# dp_clf = dp.LinearRegression()
	# inf_dp_clf = dp.LinearRegression(epsilon=float("inf"))


	# nonprivate_clf.fit(X_train, y_train)
	# nonPrivateTestScore = nonprivate_clf.score(X_test, y_test) * 100

	# dp_clf.fit(X_train, y_train)
	# dpTestScore = dp_clf.score(X_test, y_test) * 100
	# agreement = dp_clf.score(X_test, nonprivate_clf.predict(X_test)) * 100

	# inf_dp_clf.fit(X_train, y_train)
	# infDpTestScore = inf_dp_clf.score(X_test, y_test) * 100
	# infAgreement = inf_dp_clf.score(X_test, nonprivate_clf.predict(X_test)) * 100

	# print(nonPrivateTestScore, dpTestScore)