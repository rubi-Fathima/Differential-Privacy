from flask import Flask, render_template, url_for, flash, request, jsonify, send_file, redirect, session
from time import time
import csv
import json
import os

import pandas as pd
import machineLearningModule as mlm
import visualizationModule as viz
import aggregationToolsModule as agg


import diffprivlib as dp

import pickle

app = Flask(__name__)

app.config["SECRET_KEY"] = "skfnslidnfnrigenvkndsfknvikasngknd"



UPLOADED_FILE_DIR = "UploadedDatasets"
ACCOUNTANT_DIR = "ProjectAccountants"


def getDataColumns():
	fileName = os.path.join(UPLOADED_FILE_DIR, session["datasetFilename"])
	df = pd.read_csv(fileName)
	return df.columns



def getAccountantDict():
	if "accountant" in session:
		with open(session["accountant"], "rb") as f:
			acc = pickle.load(f)
			remainingBudget = list(map(lambda x: round(x, 2), acc.remaining()))
		accountantName = session["accountant"].split(".")[0].split("\\")[1]
		datasetFileName = session["datasetFilename"]
		return {"accountantName":accountantName, "remainingBudget": remainingBudget, "datasetFilename": datasetFileName}
	else:
		return {}

def saveAccountant(acc):
	with open(session["accountant"], "wb") as f:
		pickle.dump(acc, f)


@app.route("/")
def home():
	################ Viz requires acc = 9, 0
	################ Models require acc = 585, 0 for GNB
	accountantDict = getAccountantDict()
	if not accountantDict:
		if "alert" in session:
			accountantDict["alert"] = 1
			del session["alert"]
	return render_template("homePage.html", accountantDict=accountantDict)


@app.route("/aggregationToolsPage", methods=["GET", "POST"])
def aggregationToolsPage():
	if request.method == "GET":
		if "accountant" not in session:
			session["alert"] = True
			return redirect("/")
		# visualizationDict, acc = viz.getVisualization(session["dataFileName"], session["accountant"])
		aggregationDict, acc = agg.getAggregationReport(os.path.join(UPLOADED_FILE_DIR, session["datasetFilename"]), session["accountant"])
		saveAccountant(acc)	
		accountantDict = getAccountantDict()
		return render_template("/aggregationToolsPage.html", aggDict=aggregationDict, accountantDict=accountantDict)
	elif request.method == "POST":
		pass
		

@app.route("/setAccountant")
def setAccountant():
	accountantDict = getAccountantDict()
	return render_template("accountantSetup.html", accountantDict=accountantDict)


@app.route("/accountSetupCompletion", methods=["POST", "GET"])
def completeAccountantSetup():
	print("FORM:", request.form)
	# print(request.form["editColumnsCheckbox"])
	accName = request.form["accountantName"]
	accEpsilon = int(request.form["epsilonValue"])
	# accDelta = int(request.form["deltaValue"])
	acc = dp.BudgetAccountant(accEpsilon)#, accDelta)
	accountantFileName = os.path.join(ACCOUNTANT_DIR, accName+".pkl")
	with open(accountantFileName, "wb") as f:
		pickle.dump(acc, f)
		session["accountant"] = accountantFileName
	cleanDict = request.form.to_dict()
	cleanDict["datasetFilename"] = os.path.join(UPLOADED_FILE_DIR, session["datasetFilename"])
	mlm.cleanFile(cleanDict)
	return redirect("/")



@app.route("/test")
def generalFileUpload():
	# accountantDict = getAccountantDict()
	return render_template("generalFileUpload.html", accountantDict={})


@app.route("/getDatasetInfo", methods=["GET", "POST"])
def getDatasetInfo():
	if request.method == "GET":
		return "Hi"
	elif request.method == "POST":
		print(request.files["csvFile"])
		file = request.files["csvFile"]
		file.save(os.path.join(UPLOADED_FILE_DIR, file.filename))
		session["datasetFilename"] = file.filename
		print("FILENAME:", session["datasetFilename"])
		fileInfoDict = mlm.getFileInfo(os.path.join(UPLOADED_FILE_DIR, session["datasetFilename"]))
		print(fileInfoDict)
		return fileInfoDict


@app.route("/test3", methods=["GET", "POST"])
def getUploadInfo():
	if request.method == "GET":
		return "Hi"
	elif request.method == "POST":
		print("FORM DATA:")
		print(request.form)
		cleanDict = request.form.to_dict()
		cleanDict["datasetFilename"] = session["datasetFilename"]
		mlm.cleanFile(cleanDict)
		return redirect("/")



@app.errorhandler(dp.utils.BudgetError)
def budgetInvalid(error):
	accountantDict = getAccountantDict()
	return render_template("budgetInvalid.html", accountantDict=accountantDict)


@app.errorhandler(ValueError)		# Training
def invalidDataset1(error):
	print("-"*100)
	print(error)
	accountantDict = getAccountantDict()
	return render_template("datasetInvalid.html", accountantDict=accountantDict)


@app.errorhandler(TypeError)		# Summarization
def invalidDataset2(error):
	print("-"*100)
	print(error)
	accountantDict = getAccountantDict()
	return render_template("datasetInvalid.html", accountantDict=accountantDict)


@app.route("/visualizationPage", methods=["GET", "POST"])
def visualizations():
	if request.method == "GET":
		# return "Hi!"
		if "accountant" not in session:
			session["alert"] = True
			return redirect("/")
		visualizationDict, acc = viz.getVisualization(os.path.join(UPLOADED_FILE_DIR, session["datasetFilename"]), session["accountant"])
		saveAccountant(acc)	
		accountantDict = getAccountantDict()
		return render_template("/visualizationPage.html", vizDict=visualizationDict, accountantDict=accountantDict)


@app.route("/modelSelection")
def modelSelect():
	if "accountant" not in session:
		session["alert"] = True
		return redirect("/")
	dataColumns = getDataColumns()
	accountantDict = getAccountantDict()
	return render_template("modelSelect.html", dataColumns=dataColumns, accountantDict=accountantDict)


@app.route("/runModel", methods=["GET", "POST"])
def runModel():
	if request.method == "GET":
		return "Hi!"
	elif request.method == "POST":
		modelName = request.form["modelName"]
		yColumn = request.form["yColumn"]
		print("CHOOSEN MODEL:", modelName)
		resultDict, acc = mlm.getResults(os.path.join(UPLOADED_FILE_DIR, session["datasetFilename"]), yColumn, modelName, session["accountant"])
		saveAccountant(acc)	
		accountantDict = getAccountantDict()
		resultDict["warn"] = True
		print(resultDict)
		return render_template("resultsPage.html", resultDict=resultDict, accountantDict=accountantDict)

if __name__ == '__main__':
    app.run(debug=True)
