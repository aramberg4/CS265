#!/bin/bash
#File:     reextend.bash
#Purpose:  Accepts two file extensions as command line arguments and renames all files with the first
#	   extension within the current working directory to have the second extension instead
#Author:   Austin Ramberg
#Date:     April 19, 2019

if [ -z $1 ] ; then
	echo -e "\nThis program accepts two arguments. The first is the old file extension, the second is the new extension you want to change it to.\n"
	exit 1
fi

if [ -z $2 ] ; then
	echo -e "\nYou are missing the second argument for the new file extension.\n"
	exit 1
fi
for file in $(find -name "*$1") ; do
       	if [[ -f $file  ]] ; then
		echo "old file: $file"
		newFile=${file%$1*} ${file##*$1}
		newFile="$newFile$2"
		echo "new file: $newFile"
		mv $file $newFile
	fi
done
exit 0 #success
