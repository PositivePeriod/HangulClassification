import pickle
import json
import os
import shutil


class Dir:  # Directory Manager
    mainDir = "."
    inputDir = f"{mainDir}/input"
    fontsDir = f"{inputDir}/fonts"

    metaDir = f"{mainDir}/meta"
    imagesMetaDir = f"{metaDir}/images"
    featuresMetaDir = f"{metaDir}/features"

    outputDir = f"{mainDir}/output"
    imagesDir = f"{outputDir}/images"
    featuresDir = f"{outputDir}/features"
    modelsDir = f"{outputDir}/models"

    dirList = [mainDir, inputDir, fontsDir,
               metaDir, imagesMetaDir, featuresMetaDir,
               outputDir, imagesDir, featuresDir, modelsDir]

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
        newID = len(os.listdir(path))
        Dir.makeDir(f"{path}/{newID}")
        return newID

    @staticmethod
    def removeFile(path):
        content = Log.logFormat("Confirm", "Erase", f"Enter Y to erase {path} : ", show=False)
        if Dir.existFile(path) and input(content) == "Y":
            os.remove(path)

    @staticmethod
    def removeDir(path):
        content = Log.logFormat("Confirm", "Erase", f"Enter Y to erase {path} : ", show=False)
        if Dir.existDir(path) and input(content) == "Y":
            shutil.rmtree(path)

    @staticmethod
    def resetEnv():
        Dir.removeDir(Dir.metaDir)
        Dir.removeDir(Dir.outputDir)


class Log:
    stateLength = 10
    doLength = 10

    @staticmethod
    def logFormat(state, do, msg, show=True):
        assert(len(state) <= Log.stateLength)
        assert(len(do) <= Log.doLength)
        content = f"{state.ljust(Log.stateLength)} | {do.ljust(Log.doLength)} | {msg}"
        if show:
            print(content)
        else:
            return content


class File:
    fontDictPath = f"{Dir.metaDir}/fontDict.json"
    KSX1001Path = f"{Dir.inputDir}/KSX1001.txt"
    PangramPath = f"{Dir.inputDir}/pangram.txt"

    @ staticmethod
    def saveJSON(data, path):
        with open(path, "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @ staticmethod
    def loadJSON(path):
        with open(path, "r", encoding="UTF-8") as f:
            data = json.load(f)
        return data

    @ staticmethod
    def getFontDict():
        if not Dir.existFile(File.fontDictPath):
            File.saveJSON({}, File.fontDictPath)
        return File.loadJSON(File.fontDictPath)

    @ staticmethod
    def saveFontDict(data):
        File.saveJSON(data, File.fontDictPath)

    @ staticmethod
    def getFontID(fontName):
        fontDict = File.getFontDict()
        if fontName not in fontDict.keys():
            fontID = len(fontDict)
            assert fontID not in fontDict.values()
            fontDict[fontName] = fontID
            File.saveFontDict(fontDict)
        return fontDict[fontName]

    @staticmethod
    def getFontName(fontID):
        fontDict = File.getFontDict()
        if fontID in fontDict.values():
            return list(fontDict.keys())[list(fontDict.values()).index(fontID)]
        else:
            return None

    @staticmethod
    def loadTXT(path):
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
        return data

    @ staticmethod
    def getKSX1001():
        data = File.loadTXT(File.KSX1001Path)
        assert len(data) == 2350
        return data

    @ staticmethod
    def getPangram():
        data = File.loadTXT(File.PangramPath)
        return [x for x in set(data) if len(x.strip()) > 0]

    @ staticmethod
    def getFonts(path):
        extension = [".ttf", ".otf", ".TTF", ".OTF"]
        fonts = [{"name": fontPath[:-4], "path": f"{path}/{fontPath}", "id": File.getFontID(fontPath[:-4])}
                 for fontPath in os.listdir(path) if fontPath[-4:] in extension]
        return fonts

    @ staticmethod
    def savePickle(data, path):
        with open(path, "wb") as f:
            pickle.dump(data, f)

    @ staticmethod
    def loadPickle(path):
        with open(path, "rb") as f:
            data = pickle.load(f)
        return data
