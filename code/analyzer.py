from datetime import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from util import Util


class Analyzer:
    def __init__(self):
        Util.makeDir(Util.inputDir)
        Util.makeDir(Util.imagesDir)
        Util.makeDir(Util.outputDir)
        Util.makeDir(Util.modelsDir)
        Util.makeDir(Util.resultsDir)

    def loadData(self, imagesID, debug=False):
        path = f"{Util.imagesDir}/{imagesID}"
        imagesPaths = os.listdir(path)
        features = {}
        fontsName = dict()
        for imagesPath in imagesPaths:
            if imagesPath[-4:] == ".txt":
                continue  # except info.txt
            # imagesPath = font["name"]
            features[imagesPath] = np.loadtxt(
                f"{path}/{imagesPath}/analysis.csv", delimiter=",")
            fontsName[imagesPath] = len(fontsName)

        assert len(features) > 0
        fontNum = len(features)
        randomCase = list(features.values())[0]
        imageNum = randomCase.shape[0]
        featureNum = randomCase.shape[1]
        caseNum = fontNum * imageNum

        imageData = np.empty((0, featureNum), dtype=int)
        featureData = []
        for fontID, feature in features.items():
            for caseID in range(imageNum):
                caseImage = np.reshape(feature[caseID, :], (1, featureNum))
                caseName = fontsName[fontID]
                imageData = np.append(imageData, caseImage, axis=0)
                featureData.append(caseName)
        featureData = np.array(featureData)

        assert imageData.shape == (
            caseNum, featureNum) and featureData.shape == (caseNum,)
        print(Util.logFormat("Success", "Load", f"Images {imagesID}"))
        if debug:
            print(Util.logFormat("Info", "#Font", f"{fontNum}"))
            print(Util.logFormat("Info", "#Image", f"{imageNum}"))
            print(Util.logFormat("Info", "#Feature", f"{featureNum}"))
            print(Util.logFormat("Info", "#Case", f"{caseNum}"))
        return {"image": imageData, "feature": featureData, "imagesID": imagesID, "fontsName": fontsName}

    def makeOptimizedModel(self, data, gammaOption, cOption, testRatio, debug=False):
        imageData, featureData, imagesID = data["image"], data["feature"], data["imagesID"]
        # Amount of TrainData : Amount of TestData = 1-testRatio : testRatio
        xTrain, xTest, yTrain, yTest = train_test_split(
            imageData, featureData, test_size=testRatio)

        gammaTurn = (gammaOption["end"] -
                     gammaOption["start"]) / gammaOption["step"]
        cTurn = (cOption["end"] - cOption["start"]) / cOption["step"]
        turnNum = gammaTurn * cTurn  # TODO Progress bar

        sc = StandardScaler()  # Adjust data scaling
        sc.fit(xTrain)
        xTrain = sc.transform(xTrain)

        optimizeParam = None
        maxModel = None
        maxAccuracy = -np.Inf
        for gamma in np.arange(gammaOption["start"], gammaOption["end"], gammaOption["step"]):
            for c in np.arange(cOption["start"], cOption["end"], cOption["step"]):
                svm = SVC(kernel='rbf', C=c, gamma=gamma)
                svm.fit(xTrain, yTrain)
                model = {"svm": svm, "sc": sc}
                result = self.verifyModel(model, xTest, yTest)
                if result["accuracy"] > maxAccuracy:
                    optimizeParam = {"gamma": gamma, "c": c}
                    maxModel = model
                    maxAccuracy = result["accuracy"]

        model["fontsName"] = data["fontsName"]
        modelID = Util.saveModel(model)
        with open(f"{Util.imagesDir}/{imagesID}/info.txt", "r", encoding="UTF-8") as f:
            imagesInfo = f.read()
        with open(f"{Util.modelsDir}/{modelID}.txt", "w", encoding="UTF-8") as f:
            f.write(f"Time : {datetime.now()}\n")
            f.write(f"Gamma : {optimizeParam['gamma']}\n")
            f.write(f"C : {optimizeParam['c']}\n")
            f.write(f"Accuracy : {maxAccuracy}\n")
            f.write(f"TestRatio : {testRatio}\n")
            f.write(f"\nImage :\n{imagesInfo}")
        if debug:
            print(Util.logFormat("Info", "Model",
                  f"Optimized gamma {optimizeParam['gamma']}"))
            print(Util.logFormat("Info", "Model",
                  f"Optimized c {optimizeParam['c']}"))
            print(Util.logFormat("Info", "Model", f"Accuracy {maxAccuracy}"))
        return {"model": maxModel, "gamma": optimizeParam["gamma"], "c": optimizeParam["c"], "accuracy": maxAccuracy}

    def makeModel(self, c, gamma, xTrain, yTrain, xTest, yTest):
        sc = StandardScaler()  # Adjust data scaling
        sc.fit(xTrain)
        xTrain = sc.transform(xTrain)
        svm = SVC(kernel='rbf', C=c, gamma=gamma)
        svm.fit(xTrain, yTrain)
        model = {"svm": svm, "sc": sc}

        result = self.verifyModel(model, xTest, yTest)
        return {"model": model, "result": result}

    def verifyModel(self, model, xTest, yTest, debug=False):
        xTest = model["sc"].transform(xTest)
        yPrediction = model["svm"].predict(xTest)
        accuracy = np.mean(yPrediction == yTest)
        if debug:
            print(Util.logFormat("Info", "Model", f"Accuracy {accuracy}"))
            print(Util.logFormat("Info", "Model", f"Prediction {yPrediction}"))
            print(Util.logFormat("Info", "Model", f"Answer {yTest}"))
        return {"prediction": yPrediction, "answer": yTest, "accuracy": accuracy}

    def drawConfusionMatrix(self, yTrue, yPrediction, show=True):
        cm = confusion_matrix(yTrue, yPrediction)
        rowSum = cm.sum(axis=1, keepdims=True)
        print(cm, rowSum)
        normCM = cm / rowSum
        np.fill_diagonal(normCM, 0)
        if show:
            plt.matshow(cm, cmap=plt.cm.gray)
            plt.matshow(normCM, cmap=plt.cm.gray)
            plt.show()
        return normCM
