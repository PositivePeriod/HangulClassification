import time
import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from util import Dir, Log, File


class InputManager:
    def __init__(self):
        pass

    def makeImages(self, fontsID, texts, option):
        t = time.time()
        # option : fontSize, margin
        imagesID = Dir.newDir(Dir.imagesDir)
        fonts = File.loadFonts(f"{Dir.fontsDir}/{fontsID}")
        for font in fonts:
            Dir.makeDir(f"{Dir.imagesDir}/{imagesID}/{font['name']}")
            for text in texts:
                self.makeImage(font, text, f"{Dir.imagesDir}/{imagesID}/{font['name']}/{text}.png", option)
        metaData = {"time": str(datetime.now()), "runtime": time.time() - t,
                    "texts": texts, "fonts": [font["name"] for font in fonts]}
        File.saveJSON(metaData, f"{Dir.imagesMetaDir}/{imagesID}.json")
        Log.logFormat("Success", "Make", f"Images {imagesID} from Fonts {fontsID}")
        return imagesID

    def makeImage(self, font, text, path, option):
        fontFile = ImageFont.truetype(font["path"], size=option["fontSize"])  # TTF OTF 구분? TODO
        minWidth, minHeight = fontFile.getsize(text)
        width, height = minWidth + 2 * option["margin"], minHeight + 2 * option["margin"]
        image = Image.new("RGB", (width, height), color="white")
        ImageDraw.Draw(image).text((option["margin"], option["margin"]), text, font=fontFile, fill="black")
        image.save(path)

    def extractFeature(self, imagesID, size):
        t = time.time()
        featuresID = Dir.newDir(Dir.featuresDir)
        imagesMeta = File.loadJSON(f"{Dir.imagesMetaDir}/{imagesID}.json")
        for fontName in imagesMeta["fonts"]:
            features = []
            for text in imagesMeta["texts"]:
                image = Image.open(f"{Dir.imagesDir}/{imagesID}/{fontName}/{text}.png")
                features.append(self.calculate(image, size))
            np.savetxt(f"{Dir.featuresDir}/{featuresID}/{fontName}.csv", features, delimiter=",")
        featuresMeta = {"time": str(datetime.now()), "runtime": time.time() - t,
                        "texts": imagesMeta["texts"], "fonts": imagesMeta["fonts"],
                        "size": size, "featureLength": len(features[0])}
        File.saveJSON(featuresMeta, f"{Dir.featuresMetaDir}/{featuresID}.json")
        Log.logFormat("Success", "Extract", f"Features {featuresID} from Images {imagesID}")
        return featuresID

    def calculate(self, image, size):
        grayImage = image.convert("L")
        resizedImage = grayImage.resize(size, Image.NEAREST)
        resizedArray = np.array(resizedImage)
        # import pandas as pd
        # pd.DataFrame(resizedArray).to_csv(f"{Dir.outputDir}/resized.csv" , mode='w')
        # Basic Feature : return resizedArray.flatten
        # https://stackoverflow.com/questions/56987200
        xCounter = resizedArray.mean(axis=0)
        yCounter = resizedArray.mean(axis=1)
        n = len(resizedArray)
        leftDiagCounter = np.array([np.mean(np.diag(np.fliplr(resizedArray), d)) for d in range(n - 1, -n, -1)])
        rightDiagCounter = np.array([np.mean(np.diag(resizedArray, d)) for d in range(n - 1, -n, -1)])
        feature = np.concatenate((xCounter, yCounter, leftDiagCounter, rightDiagCounter))
        # print(xCounter.shape, yCounter.shape, leftDiagCounter.shape, rightDiagCounter.shape)
        # print(xCounter, yCounter, leftDiagCounter, rightDiagCounter, (feature+1)[30])
        # exit()
        feature = np.around(feature / 255 + 1, 8)[::2]
        # print(feature.shape) # (89,)
        return feature
