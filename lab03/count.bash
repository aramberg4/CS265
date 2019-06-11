#!/bin/bash
#File:     count.bash
#Purpose:  Prints out the filename, # of lines and # of words to stdout for each regular file in a directory
#Author:   Austin Ramberg
#Date:     April 19, 2019

for file in $(ls .) ; do
	if [[ -f $file  ]] ; then
		count=$( wc -l -w <"$file" )
		fileName=$( basename "$file" )
		echo $fileName $count
		
	fi
done
exit 0 #success
