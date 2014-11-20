# -*- coding: utf-8 -*-
# program: 104job.py
# description: 
# 	parse joblist from http://www.104.com.tw/area/volunteer/volunteer.cfm
# 	write the result to www/database/104job.txt
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


baseURL = "http://www.104.com.tw"
def parse104(website):
# find <td align="left">
	found = re.findall("<td align=\"left\">.*", website)
# pattern: start with 'href="', followed not ' '
	url_ptn = re.compile("(?<=href=\")[^\s]+(?!title)")
# pattern: start with '>', followed not '<'
	chinese_ptn = re.compile("(?<=>)[^<]+")

	date = [] 
# pattern: 8 digits of number followed by '<'
	for x in re.findall("\d{8}(?=\<)", website):
		date.append(x)

	data = []
	for x in found:
		if url_ptn.search(x):
			found_url = url_ptn.search(x).group(0)
			data.append(baseURL + found_url.replace('"', ''))
		if chinese_ptn.search(x):
			data.append(chinese_ptn.search(x).group(0))
	return date, data

page = 1
URL = "http://www.104.com.tw/area/volunteer/volunteer.cfm?page=" + str(page)
#html = getDataFromURL(URL)
#html = getTxtFromFile("raw.txt")

# 104job.py is executed by $HOME/www/data/parse.php,
# and parse.php is executed by /usr/bin/crontab,
# so the current path would be located where crontab is.
# That's why it's better to use absolute path.
f = open("/home/fedro/www/database/104job.txt", "w")
for page in range(1, 31):
	URL = "http://www.104.com.tw/area/volunteer/volunteer.cfm?page=" + str(page)
	html = getDataFromURL(URL)
	date, data = parse104(html)
	for x in range(len(date)):
		f.write(date[x]+"\n")		#post date
		f.write(data[x*5]+"\n")		#job url
		f.write(data[x*5+1]+"\n")	#job name
		f.write(data[x*5+2]+"\n")	#org url
		f.write(data[x*5+3]+"\n")	#org
		f.write(data[x*5+4]+"\n")	#location
print "Done! Joblist => 'www/database/104job.txt'"
