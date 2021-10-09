from inputManager import InputManager
from analyzer import Analyzer
from util import Dir, Log, File, FontDict
from functools import cmp_to_key
import time

def MAINmakeData(fontsID, texts):
    inputManager = InputManager()
    imagesID = inputManager.makeImages(
        fontsID, texts, {"fontSize": 28, "margin": 0})
    featuresID = inputManager.extractFeature(imagesID, size=(30, 30))
    return imagesID, featuresID


def MAINmakeModel(featuresID):
    analyzer = Analyzer()
    data = analyzer.loadData(featuresID)
    # g = {"start": 0.013, "end": 0.018, "step": 0.001}
    # c = {"start": 1.68, "end": 1.95, "step": 0.01}
    # Just for distinct -1 fontsID
    g = {"start": 0.013, "end": 0.018, "step": 0.01}
    c = {"start": 1.68, "end": 1.95, "step": 0.1}
    modelID = analyzer.makeOptimizedModel(data, g, c, testRatio=0.2)
    return modelID


def MAINverifyModel(modelID, featuresID):
    analyzer = Analyzer()
    data = analyzer.loadData(featuresID)

    model = File.loadPickle(f"{Dir.modelsDir}/{modelID}/model.pkl")
    result = analyzer.verifyModel(model, data["featureData"], data["answerData"])
    Log.logFormat("Info", "Verify", f"Model {modelID} by Features {featuresID}")
    Log.logFormat("Info", "      ", f"Accuracy {result['accuracy']}")

    modelMeta = File.loadJSON(f"{Dir.modelsDir}/{modelID}/meta.json")
    featuresMeta = File.loadJSON(f"{Dir.featuresMetaDir}/{featuresID}.json")

    answer = [FontDict().getFontName(fontID) for fontID in result["answer"]]
    prediction = [FontDict().getFontName(fontID) for fontID in result["prediction"]]

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
    cm, normCM = analyzer.drawConfusionMatrix(answer, prediction, labels, show=True)
    File.saveJSON({"labels": labels, "cm": cm.tolist(), "normCM": normCM.tolist()}, f"{Dir.outputDir}/figure.json")

    # import numpy as np
    # import pandas as pd
    # import seaborn as sns
    # import matplotlib.pyplot as plt
    # pdData = np.column_stack([data['featureData'], result['answer'], result["prediction"]])
    # df = pd.DataFrame(pdData)
    # corr = df.corr(method="pearson")
    # # print(corr)
    # sns.heatmap(corr, annot=False, cmap=plt.cm.Reds)
    # plt.show()
    # df.to_csv(f"{Dir.outputDir}/df.csv", mode='w')
    # corr.to_csv(f"{Dir.outputDir}/corr.csv", mode='w')


def randomHangul(n):
    import random
    return random.choices(list(set(File.loadKSX1001()) - set(File.loadPangram())), k=n)


if __name__ == "__main__":
    do, prepare, make, verify, other = False, False, False, False, False
    # Dir.resetEnv()
    # Dir.showEnv()
    Dir.prepareDir()

    do = True
    # prepare = True
    make = True
    verify = True
    # other = True
    t = time.time()
    if do:
        if prepare:
            fontsID = -1
            # texts = "안녕하세요"
            texts = File.loadPangram()
            # texts = File.loadKSX1001()
            # texts = randomHangul(20)
            imagesID, featuresID = MAINmakeData(fontsID=fontsID, texts=texts)
        if make:
            featuresID = 0
            modelID = MAINmakeModel(featuresID=featuresID)
        if verify:
            # modelID = 0
            featuresID = 1
            MAINverifyModel(modelID=modelID, featuresID=featuresID)
        if other:
            # imagesID = 1
            featuresID = InputManager().extractFeature(imagesID=imagesID, size=(30, 30))
    print(time.time()-t)
    # -1 fontsID # 183개 distinct font  - images2(아마)  - features 2
    # loadPangram - 첫 줄 지움
    #  # load 20초 이내 / 정해진 parameter에 대해 한 번 학습에 20초 - optimize 별로 안 해는데 accuracy - 0.807035519125683
    # 사실 실수로 겹치는 게 좀 있었음
     # g = {"start": 0.013, "end": 0.018, "step": 0.01} / c = {"start": 1.68, "end": 1.95, "step": 0.1}
     # optimize 사실상 없음
     # ---------------------------------------------------
    # BOKEH.ttf - 영문용 폰트 실수로 넣음
    # 창원단감
    # 나눔손글씨붓 - NanumBrush

    # 특이 사항 - 전주는 각이랑 순이랑 눈으로 구분되긴 함
    # free style 그건 그냥이랑 좀 차이남, 획 꺾어지는 이런 거 잘 파악 못하거나
    # 이상한 input, 겹치는 input이 있을 때 다른 거 학습에도 영향을 주는 듯
    # ---------------------------------------------------
    # 이상한 거 지우고 다시 해봄 -> font 개수 180개 됨!
    # images 4 - features 3 (꽤 빠름, 기다릴만함) - model2
    # 실제로는 load 중복 안 되게 최적화 필요 - load 한 번만 하고 python 말고 c로 다시 작성하면 될 것
    # g = {"start": 0.013, "end": 0.018, "step": 0.01} / c = {"start": 1.68, "end": 1.95, "step": 0.1}
    # optimize 사실상 없음
    # ---------------------------------------------------
    # delta universe도 영어 폰트였기에 제외하고 다시 해보자

    # images 5 - features 4 - model 3
    # 근데 그래도 한 번 돌리는데 이제 분 단위로 걸리는데(그래도 전체 5분 미만); gpu 등으로 가속 못 시키나?
    # tf 아니고서야 gpu 가속 지원 안 한다고 한다...
    #
    # 60sStripe
    # i am a player
    # crooked
    # 국립중앙박물관영문
    # 끝도 없이 걸리네... 하는 김에
    # 전주완판본 순
    # 도 제외
    # 183 - 9 = 174 딱 맞음
    # ---------------------------------------------------
    # reset env!
    # font -1, image 0, feature 0, model 0
    # 0.8535201149425288
    # 할매들 손글씨 폰트끼리 서로 교란
    # ---------------------------------------------------
    # 성공적이기었기에 verify!
    # randomHangul(20)! - ["뒬", "캔", "튀", "쳅", "쟉", "낍", "랬", "섀", "쌈", "녑", "풔", "쇗", "룻", "값", "샬", "촬", "샹", "둣", "찻", "팬"]
    # font -1 image 1 feature 1,2(동일함, 실수로 두 개 뽑음)
    # 0.5637931034482758 - 학습을 좀 시간 들이더라도 강화시켜야 할 듯!
