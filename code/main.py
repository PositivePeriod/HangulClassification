from inputManager import InputManager
from analyzer import Analyzer
from util import Util


def logFonts(fontsID):
    fonts = Util.getFonts(fontsID)
    for font in fonts:
        print(font["id"], font["name"])


def makeData(fontsID, texts):
    option = {"fontSize": 28, "margin": 1}
    imageSize = (30, 30)

    inputManager = InputManager()
    imagesID = inputManager.makeImages(fontsID, texts, option)
    inputManager.preprocess(imagesID, size=imageSize)


def makeModel(imagesID):
    analyzer = Analyzer()
    data = analyzer.loadData(imagesID, debug=True)
    g = {"start": 0.001, "end": 0.01, "step": 0.001}
    c = {"start": 1, "end": 1.5, "step": 0.03}
    result = analyzer.makeOptimizedModel(data, g, c, testRatio=0.2, debug=True)
    return result


def verifyModel(modelID, imagesID):
    analyzer = Analyzer()
    data = analyzer.loadData(imagesID, debug=True)
    model = Util.loadModel(modelID)
    result = analyzer.verifyModel(
        model, data["image"], data["feature"], debug=False)
    print(Util.logFormat("Info", "Model", f"Accuracy {result['accuracy']}"))
    for i, font in data["fontsName"].items():
        print(i, font)
    analyzer.drawConfusionMatrix(
        result["answer"], result["prediction"], show=True)


if __name__ == "__main__":
    Util.logStart()
    chrList = [
        # '동틀 녘 햇빛 포개짐',
        '다람쥐 헌 쳇바퀴에 타고파',
        '추운 겨울에는 따뜻한 커피와 티를 마셔야지요',
        '키스의 고유 조건은 입술끼리 만나야 하고 특별한 기술은 필요치 않다',
        '참나무 타는 소리와 야경만큼 밤의 여유를 표현해 주는 것도 없다',
        '콩고물과 우유가 들어간 빙수는 차게 먹어야 특별한 맛이 잘 표현된다',
    ]
    chrs = sorted([x for x in list(set(''.join(chrList)))
                  if x not in ['', ' ']])  # check overlapping
    chrs = list('다람쥐없다된다')
    makeData(fontsID=1, texts=chrs)

    # result = makeModel(imagesID=2)

    # logFonts(fontsID=0)
    # verifyModel(modelID=2, imagesID=1)

    # 다른 image 할 수 있게 하려면 model과 image 모두 fontsNumber 필요 ????? TODOTODTODOTODOTODOTODOTODOTODO
    Util.logFinish()
