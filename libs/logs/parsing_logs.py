

import numpy as np
import os
from shutil import copyfile

from libs.files import files
from libs.images import images
"""----------------------------------------------------------------------------------------------------

Class for parsing logs. Now it is very simple class for handling only several task cases.

----------------------------------------------------------------------------------------------------"""
class ParsedLog:
    def __init__(self):
        self.timestamp_list = []
        self.img_list = []
        self.logType_list = []
        self.data0_list = []

    def fillParsedLogFromFile(self,filepath, keyword_1, keyword_2): 
        with open(filepath, 'r', encoding='utf-8-sig') as file:
            textLog = file.read().splitlines()

        for line in textLog:
            if keyword_1 in line and 'Time:' in line and 'INFO: Recognized:' in line:
                timestamp1 = str(line).split(' sec.')[0]
                timestamp = int(timestamp1.split('Time: ')[-1])
                self.timestamp_list.append(timestamp)

                data = str(line).split(keyword_1)[0]
                data_res = data.split(keyword_2)[-1]
                self.data0_list.append(data_res)
        return self.timestamp_list, self.data0_list

    def fillParsedLogFromFolder(self,filepath, keyword_1, keyword_2):
        filename_list = files.listFilesInFolder(filepath, '.log')
        filename = filename_list[-1]
        pathFileLog = filepath + '/' + filename

        return self.fillParsedLogFromFile(pathFileLog, keyword_1, keyword_2)

    def getData0_list(self):
        return self.data0_list

    def getTimestamps(self):
        return self.timestamp_list

    def getListImages(self, folderForScanningImages, type = '.png'):
        for timest in self.timestamp_list:
            Img = folderForScanningImages + str(timest) + type
            self.img_list.append(Img)

        return self.img_list