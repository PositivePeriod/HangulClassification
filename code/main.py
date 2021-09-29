from inputManager import InputManager
from analyzer import Analyzer
from util import Dir, Log, File
from functools import cmp_to_key


def MAINmakeData(fontsID, texts):
    inputManager = InputManager()
    imagesID = inputManager.makeImages(
        fontsID, texts, {"fontSize": 28, "margin": 0})
    featuresID = inputManager.extractFeature(imagesID, size=(30, 30))
    return imagesID, featuresID


def MAINmakeModel(featuresID):
    analyzer = Analyzer()
    data = analyzer.loadData(featuresID)
    g = {"start": 0.001, "end": 0.01, "step": 0.001}
    c = {"start": 1, "end": 1.5, "step": 0.03}
    modelID = analyzer.makeOptimizedModel(data, g, c, testRatio=0.2)
    return modelID


def MAINverifyModel(modelID, featuresID):
    analyzer = Analyzer()
    data = analyzer.loadData(featuresID)
    model = File.loadPickle(f"{Dir.modelsDir}/{modelID}/model.pkl")
    result = analyzer.verifyModel(
        model, data["featureData"], data["answerData"])
    Log.logFormat("Info", "Verify",
                  f"Model {modelID} by Features {featuresID}")
    Log.logFormat("Info", "      ", f"Accuracy {result['accuracy']}")

    modelMeta = File.loadJSON(f"{Dir.modelsDir}/{modelID}/meta.json")
    featuresMeta = File.loadJSON(f"{Dir.featuresMetaDir}/{featuresID}.json")

    answer = [File.getFontName(fontID) for fontID in result["answer"]]
    prediction = [File.getFontName(fontID) for fontID in result["prediction"]]

    labels = list(set(modelMeta['fonts']) | set(featuresMeta['fonts']))

    def state(font):
        if font in modelMeta['fonts'] and font in featuresMeta['fonts']:
            return 0
        elif font in modelMeta['fonts']:
            return 1
        elif font in featuresMeta['fonts']:
            return 2
        else:
            return 3

    def compare(font1, font2):
        # change: 1 / not change: -1
        if state(font1) > state(font2):
            return 1
        elif state(font1) < state(font2):
            return -1
        else:
            if font1 < font2:
                return -1
            elif font1 > font2:
                return 1
            else:
                return 0
    labels.sort(key=cmp_to_key(compare))
    analyzer.drawConfusionMatrix(answer, prediction, labels, show=True)


if __name__ == "__main__":
    # Dir.resetEnv()
    Dir.prepareDir()

    prepare = False
    make = False
    verify = True

    if prepare:
        fontsID = 3
        texts = File.getPangram()
        # texts = File.getKSX1001()
        imagesID, featuresID = MAINmakeData(fontsID=fontsID, texts=texts)

    if make:
        # featuresID = 2
        modelID = MAINmakeModel(featuresID=featuresID)

    if verify:
        featuresID = 3
        modelID = 4
        MAINverifyModel(modelID=modelID, featuresID=featuresID)
