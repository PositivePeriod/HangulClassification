import pickle
import json
import string
import random
import os
import shutil


class Dir:  # Directory Manager
    mainDir = "."
    inputDir = f"{mainDir}/input"
    fontsDir = f"{inputDir}/fonts"
    imagesDir = f"{inputDir}/images"
    metaDir = f"{inputDir}/meta"

    outputDir = f"{mainDir}/output"
    modelsDir = f"{outputDir}/models"
    resultsDir = f"{outputDir}/results"
    dirList = [mainDir, inputDir, fontsDir, imagesDir,
               metaDir, outputDir, modelsDir, resultsDir]

    @staticmethod
    def prepareDir():
        for path in Dir.dirList:
            Dir.makeDir(path)

    @staticmethod
    def existFile(path):
        return os.path.isfile(path)

    @staticmethod
    def existDir(path):
        return os.path.isdir(path)

    @staticmethod
    def makeDir(path):
        if not os.path.isdir(path):
            os.mkdir(path)

    @staticmethod
    def newDir(path):
        os.path.

    @staticmethod
    def removeDir(path):
        text = Log.logFormat("Confirm", "Erase",
                             f"Enter Y to erase {path} : ")
        if input(text) == "Y":
            shutil.rmtree(path)

    @staticmethod
    def getDirNumber(path):
        return len(os.listdir(path))
    # Todo deprecated


class Log:
    @staticmethod
    def logFormat(state, do, msg):
        assert(len(state) <= 10)
        assert(len(do) <= 10)
        return f"{state.ljust(10)} | {do.ljust(10)} | {msg}"

    @staticmethod
    def logStart():
        print(Log.logFormat('-' * 10, '-' * 10, '-' * 30))

    @staticmethod
    def logFinish():
        print(Log.logFormat('-' * 10, '-' * 10, '-' * 30))


class File:
    fontDictPath = f"{Dir.metaDir}/fontDict.json"
    KSX1001Path = f"{Dir.inputDir}/KSX1001.txt"

    @staticmethod
    def saveJSON(data, path):
        with open(path, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def loadJSON(path):
        with open(path, 'r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def getFontDict():
        if not Dir.existFile(File.fontDictPath):
            File.saveJSON({}, File.fontDictPath)
        return File.loadJSON(File.fontDictPath)

    @staticmethod
    def saveFontDict(data):
        File.saveJSON(data, File.fontDictPath)

    @staticmethod
    def getFontID(fontName):
        fontDict = File.getFontDict()
        if fontName not in fontDict:
            fontDict[fontName] = len(fontDict)  # new FontID
            File.saveFontDict(fontDict)
        return fontDict[fontName]

    @staticmethod
    def getKSX1001():
        with open(File.KSX1001Path, "r", encoding='utf-8') as f:
            data = f.read()
        assert len(data) == 2350
        return data

    @staticmethod
    def getFonts(path):
        extension = [".ttf", ".otf", ".TTF", ".OTF"]
        fonts = [{"name": fontPath[:-4], "path": f"{path}/{fontPath}", "id": File.getFontNum(fontPath[:-4])}
                 for fontPath in os.listdir(path) if fontPath[-4:] in extension]
        return fonts

    @staticmethod
    def savePickle(data, path):
        with open(path, "wb") as f:
            pickle.dump(data, f)

    @staticmethod
    def loadPickle(path):
        with open(path, "rb") as f:
            data = pickle.load(f)
        return data


class SmallFunction:
    @staticmethod
    def getRandomHangul(n):
        return random.sample(File.getKSX1001(), n)

    @staticmethod
    def randomString(n):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))
