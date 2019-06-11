#File Name:    Album.py
#Purpose:      Class that represents a musical album.
#Author:       Austin Ramberg
#Date:         June 7, 2019
#Dependencies: None

class Album:

    #constructor
    def __init__(self, name, artist, year):
        self.__name = name
        self.__artist = artist
        self.__year = year
        self.__songList = []

    #getters
    def getName(self):
        return self.__name

    def getArtist(self):
        return self.__artist

    def getYear(self):
        return self.__year

    def getSongList(self):
        return self.__songList

    #setters
    def setSongList(self, inList):
        self.__songList = inList

    #other methods
    def appendSong(self, song):
        self.__songList.append(song)
    
    def displaySongList(self):
        for song in self.__songList:
            print(song)

    # overload __str__ method
    def __str__(self):
        return self.getArtist() + '\n' + str(self.getYear()) + ' ' + self.getName()

#for testing
if __name__ == "__main__":
    myAlbum = Album("Pet Sounds", "The Beach Boys", "1967")
    myAlbum.appendSong("Good Vibrations")
    print(myAlbum)
    myAlbum.displaySongList()
