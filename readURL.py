
# -*- coding: utf-8 -*-
import sys
import urllib2
import re

# get data from url
def getDataFromURL( url ):
	try:
		response = urllib2.urlopen(urllib2.Request(url))
	except (ValueError, urllib2.URLError) as e:
		print e
		sys.exit(0)
	temp = response.read() 
	return temp

def getTxtFromFile( filename ):
	f = open(filename, 'r')
	data = f.read()
	return data

if len(sys.argv)!=3:
	print "agrv Error."
	print "[usage]: python readandprint.py [URL] [outfile]"
	sys.exit(0)
#URL = "http://www.104.com.tw/area/volunteer/volunteer.cfm?page=1"
#URL = "http://www.104.com.tw/area/volunteer/newslist.cfm"
URL = sys.argv[1]
outfile = sys.argv[2]
html = getDataFromURL(URL)
#html = getTxtFromFile("")

f = open(outfile, "w")
f.write(html)
print "write web to "+"'"+outfile+"'"
