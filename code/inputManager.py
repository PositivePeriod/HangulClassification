import os
import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from util import Dir, Log, File, SmallFunction


class InputManager:
    def __init__(self):
        Dir.prepareDir()

    def makeImages(self, fontsID, texts, option):
        # option : fontSize, margin
        imagesID = Util.getDirNumber(Util.imagesDir)
        dirPath = f"{Util.imagesDir}/{imagesID}"
        Util.makeDir(dirPath)
        fonts = Util.getFonts(fontsID)
        for font in fonts:
            path = f"{dirPath}/{font['name']}"
            Util.makeDir(path)
            for text in texts:
                self.makeImage(font, text, path, option)
        with open(f"{dirPath}/info.txt", "w", encoding="UTF-8") as f:
            textStr = '\n'.join([' '.join(texts[i:i + 10])
                                for i in range(0, len(texts), 10)])
            fontStr = '\n'.join(font['name'] for font in fonts)
            f.write(f"Time : {datetime.now()}\n")
            f.write(f"Text : {len(texts)}\n{textStr}\n")
            f.write(f"Font : {len(fonts)}\n{fontStr}\n")
        print(Util.logFormat("Success", "Make", f"Images {imagesID}"))
        return imagesID

    def makeImage(self, font, text, path, option):
        fontFile = ImageFont.truetype(
            font['path'], size=option['fontSize'])  # TTF OTF 구분? TODO
        minWidth, minHeight = fontFile.getsize(text)

        margin = option['margin']
        width, height = minWidth + 2 * margin, minHeight + 2 * margin
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        draw.text((margin, margin), text, font=fontFile, fill='black')
        image.save(f"{path}/{text}.png")

    def preprocess(self, imagesID, size):
        path = f"{Util.imagesDir}/{imagesID}"
        imagesPaths = os.listdir(path)
        for imagesPath in imagesPaths:
            if imagesPath[-4:] == ".txt":
                continue  # info.txt
            features = []
            imagePaths = os.listdir(f"{path}/{imagesPath}")
            for imagePath in imagePaths:
                if imagePath[-4:] != ".png":
                    continue  # to ignore analysis.csv
                image = Image.open(f"{path}/{imagesPath}/{imagePath}")
                feature = self.extractFeatureFromImage(image, size)
                features.append(feature)
            np.savetxt(f"{path}/{imagesPath}/analysis.csv",
                       features, delimiter=",")
        print(Util.logFormat("Success", "Preprocess", f"Images {imagesID}"))

    def extractFeatureFromImage(self, image, size):
        grayImage = image.convert('L')
        resizedImage = grayImage.resize(size, Image.NEAREST)
        resizedArray = np.array(resizedImage)

        # Basic Feature : return resizedArray.flatten
        # https://stackoverflow.com/questions/56987200
        xCounter = resizedArray.mean(axis=0)
        yCounter = resizedArray.mean(axis=1)
        n = len(resizedArray)
        leftDiagCounter = np.array(
            [np.mean(np.diag(np.fliplr(resizedArray), d)) for d in range(n - 1, -n, -1)])
        rightDiagCounter = np.array(
            [np.mean(np.diag(resizedArray, d)) for d in range(n - 1, -n, -1)])
        feature = np.concatenate(
            (xCounter, yCounter, leftDiagCounter, rightDiagCounter))
        return feature
