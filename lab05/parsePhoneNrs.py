#!/usr/bin/env python3
#
# parsePhoneNrs.py - an example of 'grouping' - extracting parts of a match
#
# Kurt Schmidt
# 7/06
#
# Python 3.5.2
# on Linux 4.4.0-36-generic x86_64
# 
#	Demonstrates: regexp, re, search, groups
#
# Usage:  By default, reads telNrs.txt .  You may supply a different filename
#
# Notes:
#		The pattern:
#			Note that it is not perfect, but allows a bit of leeway in how we
#			write a phone #.  No extensions.
#			Of course, only handles US-style numbers
#
# EDITOR:  cols=120, tabstop=2
#

import sys
import re

stderr = sys.stderr

DEF_A_CODE = "None"

def usage() :
	print( "Usage:" )
	print( "\t" + sys.argv[0] + " [<file>]" )

def searchFile( fileName, pattern ) :

	fh = open( fileName, "r" )
	
	for l in fh :
		l = l.strip()

			# Here's the actual search
		match = pattern.search( l )

		if match :
			nr = match.groups()
				# Note, from the pattern, that 0 may be null, but 1 and 2 must exist
			if nr[0] is None :
				aCode =	DEF_A_CODE
			else :
				aCode = nr[0]
			sys.stdout.write( "area code: " + aCode + \
					", exchange: " + nr[1] + ", trunk: " + nr[2] )
                        if nr[3] is None:
                            print("")
                        else:
                            print( ", extension: " + nr[3] )
		else :
			print( "NO MATCH: " + l )
	
	fh.close()
	

def main() :

		# stick filename
	if len( sys.argv ) < 2 :  # no file name
	   # assume telNrs.txt
		fileName = "telNrs.txt"
	else :
		fileName = sys.argv[1]


		# for legibility, Python supplies a 'verbose' pattern
		#		requires a special flag (re.VERBOSE)
	#patString = '(\d{3})*[- .)]*(\d{3})[- .]*(\d{4})'

	patString = r'''
								# don't match beginning of string (takes care of 1-)
		(\d{3})?		# area code (3 digits) (optional)
		[- .)]*			# optional separator (any # of space, dash, or dot,
								#   or closing ')' )
		(\d{3})			# exchange, 3 digits
		[- .]*			# optional separator (any # of space, dash, or dot)
		(\d{4})			# number, 4 digits
                [- .x]*                 # optional separator (any # of space, dash, dot, or x)
                (\d{1,4})?              # extension, 1-4 digits (optional)
		'''

	# Here is what the pattern would look like as a regular pattern:
	#patString = r'(\d{3})\D*(\d{3})\D*(\d{4})'


	# Instead of creating a temporary object each time, we will compile this
	#		regexp once, and store this object

	pattern = re.compile( patString, re.VERBOSE )

	searchFile( fileName, pattern )

main()
