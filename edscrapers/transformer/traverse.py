import os
import json

def traverse(target):

    file_list = list()

    rootDir = './output/' + target + '/'
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            file_path = rootDir + fname
            file_list.append(file_path)

    return file_list

def read_file(file_path):

    with open(file_path, 'r') as fl:
        data = json.load(fl)
        return data