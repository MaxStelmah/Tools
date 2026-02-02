"""---------------------------------------------------------------------------------------------

    This lib contains functions for handling folders and files.

--------------------------------------------------------------------------------------------"""
import os
from shutil import copyfile
import time

# Walk around the folder and return a list of filenames
def listFilesInFolder(folder ='', type =''):

    listFiles = []
    for root, dirs, files in os.walk(folder):
        if type != '':
            for filename in files:
                if filename.endswith(type):
                    listFiles.append(filename)
        else:
            for filename in files:
                listFiles.append(filename)

    return listFiles

def listFilesInFolderWithoutSuffix(folder, suffix):

    listFiles = []
    cutLenght = len(suffix)
    # read all file names
    for root, dirs, files in os.walk(folder):
        for filename in files:                          #for all file-names
            if filename.endswith(suffix):               #cut the suffix
                filename = filename[:-cutLenght]
                listFiles.append(filename)

    return listFiles
    
# Copy the files from source folder (pathSrc) to another folder (pathDest)
def copyFilesFromPathToFolder(listFiles, pathSrc, pathDest):
    isAllSuccess = True

    for file in listFiles:
        if file is not None:
            try:
                copyfile(pathSrc+file, pathDest+file)
            except Exception as e:
                print("Error while copying file. Exaption: "+str(e))
                isAllSuccess = False
    return isAllSuccess

def clearFolder(folder):
    if not os.listdir(folder):
        print("empty")
    else:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

# Clear folder every x seconds
def keepFolderClear(folder, timeToCheck):
    while True:
        clearFolder(folder)
        time.sleep(timeToCheck)