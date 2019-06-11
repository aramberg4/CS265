#!/bin/bash
#File:     organiseMusic.bash
#Purpose:  Looks in the current directory for mp3 files, breaks the filename out into artist and song
#          title, renames the file to the name of the song and saves it to artist directory. 
#Author:   Austin Ramberg
#Date:     April 19, 2019

IFS=$'\n'

for file in $(find -maxdepth 1 -type f -name '*.mp3') ; do
	file=$( basename "$file" )
	artist=${file%%' - '*}
	echo "artist:$artist"
	song=${file#*' - '}
	echo "song:$song"
	if [[ -d $artist  ]]; then
		mv $file "$artist/$song"
	else
		mkdir $artist
		mv $file "$artist/$song"
	fi

done
exit 0 #success
