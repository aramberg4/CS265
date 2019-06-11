#File Name:    Dir.py
#Purpose:      Class that represents an OS directory. Dirs can
#              have index files, required files, and other files. 
#Author:       Austin Ramberg
#Date:         May 28, 2019
#Dependencies: File.py

from File import File
class Dir:

    #constructor
    def __init__(self, index = None):
        self.__index = index
        self.__reqList = []
        self.__otherList = []

    #getters
    def getIndex(self):
        return self.__index

    def getReqList(self):
        return self.__reqList

    def getOtherList(self):
        return self.__otherList

    #setters
    def setIndex(self, inFile):
        self.__index = inFile

    def setReqList(self, inList):
        self.__reqList = inList

    def setOtherList(self, inList):
        self.__otherList = inList

    #other methods
    def appendReqList(self, inFile):
        self.__reqList.append(inFile)

    def appendOtherList(self, inFile):
        self.__otherList.append(inFile)

#for testing
if __name__ == "__main__":
    index = File("index.html", "file")
    r1 = File("r1", "file")
    r2 = File("r2", "file")
    reqList = [r1, r2]
    misc = File("misc.txt", "file")
    otherList = [misc]
    myDir = Dir(index, reqList, otherList)
    r3 = File("r3", "file")
    myDir.appendRequired(r3)
    print(myDir.getIndex())
    for req in myDir.getReqList():
        print(req)
    for oth in myDir.getOtherList():
        print(oth)


