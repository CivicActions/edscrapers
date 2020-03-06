import os
import json

def traverse(target):

    file_list = list()

    rootDir = './output/' + target + '/'
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            
            if "print" in fname.split("-"):
                continue

            file_path = rootDir + fname
            file_list.append(file_path)

    #file_path = './output/ocr/statenationalestimations-estimations-2011-12-ec1f37db9facab42f97f909f12439a28-1fcf6afb6294aa0088db0bef6a2d95a3.json'
    #file_list = list()
    #file_list.append(file_path)

    return file_list

def read_file(file_path):

    with open(file_path, 'r') as fl:
        data = json.load(fl)
        return data