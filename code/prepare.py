import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class Util:
    mainDir = "."
    fontDir = f"{mainDir}/font"
    inputDir = f"{mainDir}/input"
    @staticmethod
    def getFonts():
        fontPaths = sorted(os.listdir(Util.fontDir))
        fonts = [{"name": fontPath[:-4], "path": f"{Util.fontDir}/{fontPath}", "id": i} for i, fontPath in enumerate(fontPaths) if fontPath[-4:] in [".ttf", ".otf"]]
        return fonts

    def checkDir(path):
        if not os.path.isdir(path):
            os.mkdir(path)

class InputMaker:
    def __init__(self):
        Util.checkDir(Util.inputDir)

    def makeInput(self, texts, fontSize):
        fonts = Util.getFonts()
        for font in fonts:
            for text in texts:
                self.makeImage(text, font, fontSize)
        print('InputMaker.makeInput Finished\n')

    def makeImage(self, text, font, fontSize):
        # TTF OTF 구분? TODO
        fontFile = ImageFont.truetype(font['path'], size=fontSize)
        
        margin = 1
        minWidth, minHeight = fontFile.getsize(text)
        width = minWidth + 2*margin
        height = minHeight + 2*margin

        image =Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        draw.text((margin, margin), text, font=fontFile, fill='black')

        Util.checkDir(f"{Util.inputDir}/{font['name']}")
        image.save(f"{Util.inputDir}/{font['name']}/{font['name']} {text}.png")

class InputPreprocessor:
    def __init__(self):
        pass
        # Already checked in InputMaker
        # Util.checkDir(Util.inputDir)
        # fonts = Util.getFonts()
        # for font in fonts:
        #     Util.checkDir(f"{Util.inputDir}/{font['name']}")

    def preprocess(self, size):
        fonts = Util.getFonts()
        for font in fonts:
            features = []
            inputPath = f"{Util.inputDir}/{font['name']}"
            imagePaths = os.listdir(inputPath)
            for imagePath in imagePaths:
                if imagePath[-4:] != ".png": continue # ignore analysis.csv
                image = Image.open(f"{inputPath}/{imagePath}")
                feature = self.extractFeatureFromImage(image, size)
                features.append(feature)
            # print(features[0].shape)
            np.savetxt(f"{Util.inputDir}/{font['name']}/analysis.csv", features, delimiter=",")
        print('InputPreprocessor.preprocess Finished\n')

    def extractFeatureFromImage(self, image, size):
        grayImage = image.convert('L')
        resizedImage = grayImage.resize(size, Image.NEAREST)
        resizedArray = np.array(resizedImage)

        # Basic Feature : return resizedArray.flatten
        # https://stackoverflow.com/questions/56987200
        xCounter = resizedArray.mean(axis=0)
        yCounter = resizedArray.mean(axis=1)
        n = len(resizedArray)
        leftDiagCounter = np.array([np.mean(np.diag(np.fliplr(resizedArray), d)) for d in range(n-1, -n, -1)])
        rightDiagCounter = np.array([np.mean(np.diag(resizedArray, d)) for d in range(n-1, -n, -1)])
        feature = np.concatenate((xCounter, yCounter, leftDiagCounter, rightDiagCounter))
        return feature