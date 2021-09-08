import numpy as np
from prepare import Util
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


class Analyzer:
    def __init__(self):
        pass

    def loadData():
        fonts = Util.getFonts()
        features = {}
        for font in fonts:
            features[font['id']] = np.loadtxt(f"{Util.inputDir}/{font['name']}/analysis.csv", delimiter=",")

        fontNum = len(features)
        imageNum = features[0].shape[0]
        featureNum = features[0].shape[1]
        caseNum = fontNum * imageNum

        imageData = np.empty((0, featureNum), dtype=int)     
        featureData = []
        for fontID, feature in features.items():
            for caseID in range(imageNum):
                caseImage = np.reshape(feature[caseID,:],(1, featureNum))
                caseName = fontID
                imageData = np.append(imageData, caseImage, axis=0)
                featureData.append(caseName)
        featureData = np.array(featureData)

        assert imageData.shape == (caseNum, featureNum) and featureData.shape == (caseNum,)
        print(f"Number of font : {fontNum}")
        print(f"Number of image : {imageNum}")
        print(f"Number of feature : {featureNum}")
        print(f"Number of case : {caseNum}")
        print('Analyzer.loadData Finished\n')
        return {"image": imageData, "feature": featureData}

    def analyze(self, optimal, gammaOption, cOption, testRatio):
        data = Analyzer.loadData()
        imageData, featureData = data["image"], data["feature"]

        # Amount of TrainData : Amount of TestData = 1-testRatio : testRatio
        xTrain, xTest, yTrain, yTest = train_test_split(imageData, featureData, test_size = testRatio)

        # Normalization?
        sc = StandardScaler()
        sc.fit(xTrain)
        xTrain = sc.transform(xTrain)
        xTest = sc.transform(xTest)

        optimal = self.optimizeTraining(optimal, gammaOption, cOption, xTrain, yTrain, xTest, yTest)
        self.training(optimal["c"], optimal["gamma"], xTrain, yTrain, xTest, yTest, debug=True)
        print('Analyzer.analyze Finished\n')

    def training(self, c, gamma, xTrain, yTrain, xTest, yTest, debug=False):
        model = SVC(kernel='rbf', C=c, gamma=gamma)
        model.fit(xTrain, yTrain)
        yPrediction = model.predict(xTest)
        accurarcy = np.mean(yPrediction == yTest)
        r2 = model.score(xTest, yTest) # coefficient of determination
        if debug:
            print(f"Prediction   : {yPrediction}")
            print(f"Ground truth : {yTest}")
            print(f"Accuracy     : {accurarcy}")
            print(f"R2           : {r2}")
        return {"accuracy": accurarcy, "r2": r2}

    def optimizeTraining(self, optimal, gammaOption, cOption, xTrain, yTrain, xTest, yTest):
        gammaTurn = (gammaOption["end"]-gammaOption["start"])/gammaOption["step"]
        cTurn = (cOption["end"]-cOption["start"])/cOption["step"]
        print(f'Number of turn : {gammaTurn * cTurn}')

        counter = 0
        for gamma in np.arange(gammaOption["start"], gammaOption["end"], gammaOption["step"]):
            for c in np.arange(cOption["start"], cOption["end"], cOption["step"]):
                counter += 1
                if (counter % 10 == 0):
                    print(counter, end=" ") # end="\r"
                result = self.training(c, gamma, xTrain, yTrain, xTest, yTest)
                if result["accuracy"] > optimal["accuracy"]:
                    optimal = {"gamma": gamma, "c": c, "accuracy": result["accuracy"],"r2": result["r2"]}
        print() # end=" "
        print(f"Optimal gamma : {optimal['gamma']}")
        print(f"Optimal c     : {optimal['c']}")
        # print(f"Optimal acc   : {optimal['accuracy']}")
        # print(f"Optimal r2    : {optimal['r2']}")
        return optimal