"""---------------------------------------------------------------------------------------------

    This lib contains functions for handling images.

--------------------------------------------------------------------------------------------"""

from PIL import Image
import cv2
import os
from shutil import copyfile

from libs.files.files import *

# Compare two images and return the difference (in persent)
def compareTwoImages(image1, image2):

    i1 = Image.open(image1)
    i2 = Image.open(image2)
    assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."

    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    ncomponents = i1.size[0] * i1.size[1] * 3
    persentDif = (dif / 255.0 * 100) / ncomponents
    #print("Difference (percentage):", persentDif)
    return persentDif

def findDifferentImagesInFolder(folderForScanningImages, filterPersent):

    listFiles = FilesLib.listFilesInFolder(folderForScanningImages, ".png")
    print("All analising files: ")
    print(listFiles)

    listDifferentFiles = []

    print("Scaning...")
    for file in listFiles:
        if listFiles.index(file) == 0:
            listDifferentFiles.append(file)
            prev_file = file
            print(prev_file)
            continue
        else:
            # print(prev_file)
            print(file)
            persDiffenrence = compareTwoImages(folderForScanningImages+prev_file, folderForScanningImages+file)
            if persDiffenrence > filterPersent :
                listDifferentFiles.append(file)
            prev_file = file

    print("Different files: ")
    print(listDifferentFiles)
    return listDifferentFiles

def copyDifferentImages(folderForScanningImages, folderForResImages, filterPersent):
    listImages = findDifferentImagesInFolder(folderForScanningImages, filterPersent)
    FilesLib.copyFilesFromPathToFolder(listImages, folderForScanningImages, folderForResImages)

def blendImages(pathImg1, alfaImg1, pathImg2, alfaImg2, pathImgRes):
    img1 = cv2.imread(pathImg1)
    img2 = cv2.imread(pathImg2)
    
    try:
        dst = cv2.addWeighted(img1, alfaImg1, img2, alfaImg2, 0)
        cv2.imwrite(pathImgRes, dst)
        return dst
    except Exception as e:
        print('Error during blending images. Exception: ' + str(e))
        return e
    
