# -*- coding: utf-8 -*-
# program: 104jobdet.py
import sys
import urllib2
import re

def getTxtFromFile( filename ):
	f = open( filename, 'r' )
	data = f.read()
	# remove '\r' character
	data = data.replace('\r', '')
	return data

def parse104(website):
	# match the strings
	# begin with "<div class=\"intro\">" or "<div class=\"interview\">"
	# end with "<div class=\"intro\">" or "<div class=\"interview\">" or "<script type"
	# (?s) means re.DOTALL
	# (?:...) means non-capturing mode
	found = re.findall("(?s)(<div class=\"(?:intro|interview)\">(?:.(?!<script type|<div class=\"(?:intro|interview)))*)", website)

	data = []
	for x in found:
		data.append( re.sub("<[^>]*>|[ \t]+|#(?<=#).*","",str(x)) )
		#data.append(x)
	return data



if len(sys.argv)!=2:
	print "agrv Error."
	print "[usage]: python [inputHtml]"
	sys.exit(0)

infile = sys.argv[1]
htmlfile = getTxtFromFile(infile)
data = parse104(htmlfile)
#f = open("replace.txt", "w")
#f.write(data)
#print data
cnt=1
print data[1:]
'''
for i in data:
	print cnt
	print re.sub(r"^\s+$","",i)
	for j in re.split("\n",i):
		if len(j)>0:
			print j
	cnt+=1
'''
'''
for i in data[1]:
	print str(ord(i))+ ' '
'''
