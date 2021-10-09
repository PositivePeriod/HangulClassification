import os
from util import Dir
import shutil

assetPath = r"C:\Users\jeukh\Documents\GitHub\HangulClassification\data\asset\OpenFont_EasyToUse_Distinct"

fontList = [] # [directory, name]
for subpath in os.listdir(assetPath):
    if os.path.isdir(assetPath+f"\{subpath}"):
        subfont = os.listdir(assetPath+f'\{subpath}')[0]
        fontPath = [f"\{subpath}\{subfont}", f"\{subfont}"]
    else:
        fontPath = [f"\{subpath}", f"\{subpath}"]
    fontList.append(fontPath)
print(fontList, len(fontList)) # 183 distinct family font

newPath = Dir.fontsDir+f"\{-1}"
os.mkdir(newPath)
for font in fontList:
    # print(assetPath+font[0], newPath+font[1])
    shutil.copy(assetPath+font[0], newPath+font[1])