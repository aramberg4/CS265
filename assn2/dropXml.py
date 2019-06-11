#File Name:    dropXml.py
#Purpose:      Program that recursively walks through a directory tree 
#              and drops dir.xml files, harvesting data from possible READMEs
#Dependencies: File.py, Dir.py
#Author:       Austin Ramberg
#Date:         May 28, 2019
#Sources:
# https://stackabuse.com/python-check-if-a-file-or-directory-exists/
# https://www.geeksforgeeks.org/os-walk-python/
# https://www.guru99.com/reading-and-writing-files-in-python.html#1
# 

import sys, os, stat
from Dir import Dir
from File import File

#check if readme exists
def readMeExists(inDir):
    return os.path.exists(inDir+'/README')

#harvest README
def extractIndex(inDir):
    index = None
    with open(inDir+'/README', 'r') as fh:
        for line in fh:
            line = line.strip('\n')
            lineList = line.split(":")
            if(lineList[0] == 'index'):
                index = lineList[1]
    return index

def extractRequired(inDir):
    reqs = set()
    with open(inDir+'/README', 'r') as fh:
        for line in fh:
            line = line.strip('\n')
            lineList = line.split(":")
            if(lineList[0] == 'required'):
                reqs = set(lineList[1:])
    return reqs

#create a Dir object for the directory
def createDirObject(inDir, reqs):
    newDir = Dir()
    dirList = os.listdir(inDir)
    for item in dirList:
        newFile = createFileObject(item, inDir)
        if(newFile.getFileName() in reqs):
            newDir.appendReqList(newFile)
        elif(newFile.getFileName() == 'dir.xml'):
            #fake news
            pass
        else:
            newDir.appendOtherList(newFile)
    return newDir

#create file object given name and path
def createFileObject(name, path):
    fileType = ''
    filePath = path+'/'+name
    filePath = filePath.rstrip('\n')
    mode = os.stat(filePath).st_mode
    if(stat.S_ISSOCK(mode)):#file is a socket
        fileType = 'sock'
    elif(stat.S_ISFIFO(mode)):#file is a pipe
        fileType = 'fifo'
    elif(os.path.isdir(filePath)):#file is a dir
        fileType = 'dir'
    else:# file is a file
        fileType = 'file'
    rFile = File(name, fileType)
    return rFile

#generate dir.xml file from a Dir object
def generateXml(inDir, dirObject):
    #clear previous dir.xml, if it exists
    fh = open(inDir+"/dir.xml","w+")
    fh.write('')
    fh.close()
    #append lines to new dir.xml
    fh = open(inDir+"/dir.xml","a+")
    try:
        fh.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
        fh.write('<direntry>\n')
        if(dirObject.getIndex() != None):
            fh.write('  <index>\n')
            fh.write('      '+str(dirObject.getIndex())+'\n')
            fh.write('  </index>\n')
        if(len(dirObject.getReqList()) > 0):
            fh.write('  <required>\n')
            for req in dirObject.getReqList():
                fh.write('      '+str(req)+'\n')
            fh.write('  </required>\n')
        if(len(dirObject.getOtherList()) > 0):
            fh.write('  <other>\n')
            for oth in dirObject.getOtherList():
                fh.write('      '+str(oth)+'\n')
            fh.write('  </other>\n')
        fh.write('</direntry>\n')
        fh.close()
        print('dir.xml file generated successfully.')
    except Exception as e:
        print('Error while attempting to drop dir.xml file: '+ str(e))
        fh.close()

def main():            
    #parse cmd args
    if(len(sys.argv) == 2 ):
        dirPath = sys.argv[1]
    else:
        dirPath = os.getcwd()
    #recurse with os.walk()
    for root, dirs, files in os.walk(dirPath):
        index = None
        reqNameSet = set()
        print('Directory: '+str(root))
        #check for README
        if(readMeExists(root)):
            print('Directory has a README')
            index = extractIndex(root)
            reqNameSet = extractRequired(root)
        else:
            print('Directory does NOT have a README')
        #create Dir object
        thisDir = createDirObject(root, reqNameSet)
        #set index
        if(index != None):
            indexFile = createFileObject(index, root)
            thisDir.setIndex(indexFile)
            print('index:')
            print(thisDir.getIndex())
        print('Required:')
        for req in thisDir.getReqList():
            print(req)
        print('Other:')
        for oth in thisDir.getOtherList():
            print(oth)
        #drop dir.xml file
        generateXml(root, thisDir)
        print('')

if __name__ == "__main__":
    main()
