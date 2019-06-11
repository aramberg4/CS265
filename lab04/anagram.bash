#!/bin/bash
#File:     anagram.bash
#Purpose:  Prints out the top 10 anagram classes from words found in /usr/share/dict/words
#Author:   Austin Ramberg
#Date:     April 25, 2019

#check if the c program sign.c exits
if [ -e sign.c ]
then
	#compile
	gcc -osign sign.c
else
	echo "sign.c not found"
	exit 1
fi

#check if squash.awk exists
if [ -e squash.awk ]
then
	#collect all adjacent words with the same key
	./sign < /usr/share/dict/words | sort | awk -f squash.awk > out
else
	echo "squash.awk not found"
	exit 1
fi
#sort anagram classes by word count and output top 10
awk '{ print NF " " $0}' < out | sort -n | tail
exit 0
