#!/usr/bin/python3.6

#File Name:    cddb.py
#Purpose:      Maintains a flat-file database of album information
#Author:       Austin Ramberg
#Date:         June 7, 2019
#Dependencies: Album.py
#Sources:
#https://www.geeksforgeeks.org/sorted-function-python/
#https://wiki.python.org/moin/HowTo/Sorting
#https://stackoverflow.com/questions/20063/whats-the-best-way-to-parse-command-line-arguments
#https://stackoverflow.com/questions/10269701/case-insensitive-list-sorting-without-lowercasing-the-result

import os
from Album import Album
import argparse

#convert formatted db file to dictionary of albums
def file2Dict(filePath):
    d = dict()
    dbFile = open(filePath,'r')
    dbText = dbFile.read()
    dbtext = dbText.strip()
    dbList = dbText.split("\n\n")
    for album in dbList:
        albumLines = album.split("\n")
        i = 0
        for albumLine in albumLines:
            if(i == 0):
                artist = albumLine.strip()
            elif(i == 1):
                words = albumLine.split()
                year = words[0].strip()
                name = albumLine.strip(year)
                name = name.strip()
                year = int(year)
                newAlbum = Album(name, artist, year)
            else:
                song = albumLine.strip('-')
                song = song.strip()
                if(song == ''):
                    continue #splitting on last line will create blank song, ignore this
                else:
                    newAlbum.appendSong(song)
            i+=1
        if(newAlbum.getArtist() in d):
            d[newAlbum.getArtist()].append(newAlbum)
        else:
            d[newAlbum.getArtist()] = []
            d[newAlbum.getArtist()].append(newAlbum)
    return d

#convert dictioanry of albums to formatted db file
def dict2File(inDict, dbFilePath):
    #clear previous db.tmp, if it exists
    cwd = os.getcwd()
    tempFile = cwd+ "/db.tmp"
    fh = open(tempFile,"w+")
    fh.write('')
    fh.close()
    #append lines to new db.tmp
    fh = open(tempFile,"a+")
    try:
        for artist in inDict:
            for album in inDict[artist]:
                fh.write(str(album)+ '\n')
                for song in album.getSongList():
                    fh.write('-'+song+'\n')
                fh.write('\n')
        fh.close()

        #Go through hell and back to remove one line
        readFile = open(tempFile)
        lines = readFile.readlines()
        readFile.close()
        w = open(tempFile,'w')
        w.writelines([item for item in lines[:-1]])
        w.close()

        #create backup
        os.rename(dbFilePath,dbFilePath+'.bak')
        #save temp file as new db file
        os.rename(tempFile, dbFilePath)
        print('Database file successfully modified.')
    except Exception as e:
        print('Error while attempting to update the database. Changes not saved. See error: '+ str(e))
        fh.close()

#add album to dictionary and save to db file
def addAlbum(inDict, dbFilePath):
    name = input('Please enter the name of the album: ')
    while True:
        try:
            year = int(input('Please enter release year: '))
        except:
            print('Year must be an integer!')
            continue
        break
    artist = input('Please enter the artist: ')
    newAlbum = Album(name, artist, year)
    while True:
        newSong =  input('Please add a song or type "q" to stop: ')
        if(newSong == 'q'):
            break
        else:
            newAlbum.appendSong(newSong)
    if(newAlbum.getArtist() not in inDict):
        inDict[newAlbum.getArtist()] = []
        inDict[newAlbum.getArtist()].append(newAlbum)
    else:
        albumFound = False
        for album in inDict[newAlbum.getArtist()]:
            if(album.getName() == newAlbum.getName()):
                albumFound = True
        if(albumFound):
            print('Album already exists! Aborting.')
        else:
            inDict[newAlbum.getArtist()].append(newAlbum)
            dict2File(inDict, dbFilePath)

#Display an enumerated, alphabetical list of artists
def displayArtists(inDict, deleteMode, dbFilePath):
    artistList = []
    i = 1
    for key in inDict:
        artistList.append(key)
    artistList = sorted(artistList, key=lambda s: s.lower())
    for artist in artistList:
        print(str(i)+'. '+artist)
        i+=1
    #Allow the user to choose an artist by entering the number, or to quit by entering a q
    inputArtist = str(input('Please enter the number next to the artist you would like to browse or "q" to exit: '))
    if(inputArtist == 'q'):
        return
    else:
        inputArtist = int(inputArtist)
        inputArtist = artistList[inputArtist -1]
        displayAlbums(inputArtist, inDict, deleteMode)

#List all albums, by release date, enumerated
def displayAlbums(inArtist, inDict, deleteMode):
    albumList = []
    i = 1   
    for album in sorted(inDict[inArtist], key=lambda album: album.getYear()):
        albumList.append(album.getName())
        print(str(i)+'. '+str(album.getYear())+' - '+album.getName())
        i += 1
    #Allow the user to choose an album, by #, or return to the menu above (artists) by entering a
    if(deleteMode):
        inputAlbum = input('Please enter the number next to the album you would like to delete or "a" to return to artists: ' )
        if(inputAlbum =='a'):
            displayArtists(inDict, True, dbFilePath)
        else:
            inputAlbum = int(inputAlbum)
            inputAlbum = albumList[inputAlbum - 1]
            for album in inDict[inArtist]:
                if(album.getName() == inputAlbum):
                    inDict[inArtist].remove(album)
                    print('Album removed!')
                    print('Modifying db file...')
                    dict2File(inDict, dbFilePath)
                    return
    else:
        inputAlbum = str(input('Please enter the number next to the album you would like to browse or "a" to return to artists: '))
        if(inputAlbum == 'a'):
            displayArtists(inDict, False, dbFilePath)
        else:
            inputAlbum = int(inputAlbum)
            inputAlbum = albumList[inputAlbum - 1]
            displaySongs(inputAlbum, inArtist, inDict)

#List all songs in that album, by track order.
def displaySongs(inAlbum, inArtist, inDict):
    for album in inDict[inArtist]:
        if(album.getName() ==  inAlbum):
            album.displaySongList()
    #Prompt for input to return to the previous (i.e., the album) menu
    prompt = str(input('Press any key to return to albums menu: '))
    displayAlbums(inArtist, inDict, False)

#Print out the dictionary for testing purposes
def printDict(inDict):
    for artist in albumDict:
        for album in albumDict[artist]:
            print(album)
            for song in album.getSongList():
                print('-'+song)

#main
if __name__ == "__main__":
    #Parse options
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', action='store_true', help='List album')
    parser.add_argument('-a', action='store_true', help='Add album')
    parser.add_argument('-d', action='store_true', help='Delete album')
    args = parser.parse_args()

    #Get db file location from exported env var
    dbFilePath = os.environ['CDDB']

    #Load db into dictionary data structure
    albumDict = file2Dict(dbFilePath)

    #Perform the appropriate task
    if(args.l):
        displayArtists(albumDict, False, dbFilePath)
    elif(args.a):
        addAlbum(albumDict, dbFilePath)
    elif(args.d):
        displayArtists(albumDict, True, dbFilePath)



