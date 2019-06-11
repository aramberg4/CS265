#File Name:   File.py
#Purpose:     A class that represents a file/item in a directory. 
#             This can either be a file, directory, pipe, or socket.
#Author:      Austin Ramberg
#Date:        May 28, 2019

class File:
    #constructor
    def __init__(self, inName, inType):
        self.__fileName = inName
        self.__fileType = inType

    #getters
    def getFileName(self):
        return self.__fileName

    def getFileType(self):
        return self.__fielType

    #other methods
    def __str__(self):
        return '<'+self.__fileType+'>'+self.__fileName+'</'+self.__fileType+'>'

#for testing
if __name__ == "__main__":
    name = "myFile.txt"
    t = "file"
    myFile = File(name, t)
    print(myFile)

