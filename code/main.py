import numpy as np
from prepare import Util, InputMaker, InputPreprocessor
from analysis import Analyzer

if __name__ == "__main__":
    for font in Util.getFonts():
        print(font)
    print()

    wantToMakeData = False
    wantToAnalyze = True

    if wantToMakeData:
        # check overlapping
        chrList = [
            '가나다라마바사아자차카타파하',
            '동틀 녘 햇빛 포개짐'
            '다람쥐 헌 쳇바퀴에 타고파',
            '추운 겨울에는 따뜻한 커피와 티를 마셔야지요',
            '키스의 고유 조건은 입술끼리 만나야 하고 특별한 기술은 필요치 않다',
            '참나무 타는 소리와 야경만큼 밤의 여유를 표현해 주는 것도 없다',
            '콩고물과 우유가 들어간 빙수는 차게 먹어야 특별한 맛이 잘 표현된다',
        ]
        chrs = [x for x in list(set(''.join(chrList))) if len(x) > 0]
        # print(chrs)
        InputMaker().makeInput(texts=chrs, fontSize=28)

        InputPreprocessor().preprocess(size = (40, 40))

    if wantToAnalyze:
        opt = {"gamma": 0, "c": 0, "accuracy": -np.Inf,"r2": -np.Inf}
        g = {"start": 0.001, "end": 0.01, "step": 0.001}
        c = {"start": 1, "end": 1.5, "step": 0.03}
        testRatio = 0.4
        Analyzer().analyze(optimal=opt, gammaOption=g, cOption=c, testRatio=0.8)