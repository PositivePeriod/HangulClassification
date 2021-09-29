from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import size
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from util import Dir, Log, File


class Analyzer:
    def __init__(self):
        pass

    def loadData(self, featuresID):
        meta = File.loadJSON(f"{Dir.featuresMetaDir}/{featuresID}.json")
        featureData = np.empty((0, meta["featureLength"]), dtype=int)
        answerData = []
        for fontName in meta["fonts"]:
            fontID = File.getFontID(fontName)
            answerData.extend([fontID] * len(meta["texts"]))
            data = np.loadtxt(f"{Dir.featuresDir}/{featuresID}/{fontName}.csv", delimiter=",")
            for i in range(len(meta["texts"])):
                featureData = np.append(featureData, np.reshape(data[i, :], (1, meta["featureLength"])), axis=0)
        answerData = np.array(answerData)

        assert len(answerData) > 0 \
            and featureData.shape == (len(meta["fonts"]) * len(meta["texts"]), meta["featureLength"]) \
            and answerData.shape == (len(meta["fonts"]) * len(meta["texts"]),)
        Log.logFormat("Success", "Load", f"Features {featuresID}")
        return {"featureData": featureData, "answerData": answerData, "featuresID": featuresID}

    def makeOptimizedModel(self, data, gOpt, cOpt, testRatio):
        featureData, answerData, featuresID = data["featureData"], data["answerData"], data["featuresID"]
        # Amount of TrainData : Amount of TestData = 1-testRatio : testRatio
        xTrain, xTest, yTrain, yTest = train_test_split(featureData, answerData, test_size=testRatio)

        best = {"gamma": None, "c": None, "model": None, "accuracy": -np.Inf}
        for gamma in np.arange(gOpt["start"], gOpt["end"], gOpt["step"]):
            for c in np.arange(cOpt["start"], cOpt["end"], cOpt["step"]):
                model = self.makeModel(c, gamma, xTrain, yTrain)
                result = self.verifyModel(model, xTest, yTest)
                if result["accuracy"] > best["accuracy"]:
                    best = {"gamma": gamma, "c": c, "model": model, "accuracy": result["accuracy"]}

        modelID = Dir.newDir(Dir.modelsDir)
        File.savePickle(best["model"], f"{Dir.modelsDir}/{modelID}/model.pkl")
        featuresMeta = File.loadJSON(f"{Dir.featuresMetaDir}/{featuresID}.json")
        modelMeta = {
            "time": str(datetime.now()), "gamma": best["gamma"], "c": best["c"],
            "accuracy": best["accuracy"], "ratio": testRatio,
            "texts": featuresMeta["texts"], "fonts": featuresMeta["fonts"], "size": featuresMeta["size"]}
        File.saveJSON(modelMeta, f"{Dir.modelsDir}/{modelID}/meta.json")
        Log.logFormat("Success", "Make", f"Model {modelID} from Features {data['featuresID']}")
        return modelID

    def makeModel(self, c, gamma, xTrain, yTrain):
        sc = StandardScaler()  # Adjust data scaling
        sc.fit(xTrain)
        xTrain = sc.transform(xTrain)
        svm = SVC(kernel="rbf", C=c, gamma=gamma)
        svm.fit(xTrain, yTrain)
        return {"svm": svm, "sc": sc}

    def verifyModel(self, model, xTest, yTest):
        xTest = model["sc"].transform(xTest)
        yPrediction = model["svm"].predict(xTest)
        accuracy = np.mean(yPrediction == yTest)
        return {"prediction": yPrediction, "answer": yTest, "accuracy": accuracy}

    def drawConfusionMatrix(self, yTrue, yPrediction, labels, show=True):
        plt.rc('font', family='Malgun Gothic', size="7")  # Hangul Font
        for fontName in labels:
            print('True', labels, yTrue.count(fontName))
        for fontName in labels:
            print('Pred', labels, yPrediction.count(fontName))

        cm = confusion_matrix(yTrue, yPrediction, labels=labels)
        rowSum = cm.sum(axis=1, keepdims=True)
        print("CM : \n", cm)
        print("rowSum :", rowSum.tolist())
        normCM = cm / np.where(rowSum > 0, rowSum, 1)
        np.fill_diagonal(normCM, 0)
        if show:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            cax = ax.matshow(cm, cmap=plt.cm.gray)
            fig.colorbar(cax)
            ax.set_xticks(np.arange(len(labels)))
            ax.set_yticks(np.arange(len(labels)))
            ax.set_xticklabels(labels)
            ax.set_yticklabels(labels)

            fig = plt.figure()
            ax = fig.add_subplot(111)
            cax = ax.matshow(normCM, cmap=plt.cm.gray)
            fig.colorbar(cax)
            ax.set_xticks(np.arange(len(labels)))
            ax.set_yticks(np.arange(len(labels)))
            ax.set_xticklabels(labels)
            ax.set_yticklabels(labels)
            plt.show()
        return normCM
