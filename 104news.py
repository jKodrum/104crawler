# -*- coding: utf-8 -*-
# program: 104news.py
# description: 
# 	parse joblist from http://www.104.com.tw/area/volunteer/newslist.cfm
# 	write the result to www/database/104news.txt
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


baseURL = "http://www.104.com.tw/area/volunteer/"
def parse104(website):
	date = [] 
# pattern: 8 digits of number followed by '<'
	for x in re.findall("\d{8}(?=\<)", website):
		date.append(x)

	newsurl = []
	news = []
# pattern: start with 'href="', followed not ' '
	url_ptn = re.compile("(?<=href=\")[^\s]+(?!title)")
# pattern: start with '>', followed not '<'
	chinese_ptn = re.compile("(?<=>)[^<]+")
	matches = re.findall("<td width=\"45%\" align=\"left\">.*", website)
	for x in matches:
		matchurl = url_ptn.search(x)
		if matchurl:
			newsurl.append(baseURL + matchurl.group(0).replace('"', ''))
		news.append(chinese_ptn.search(x).group(0))

	org = []
	preptn = "<td width=\"32%\" align=\"left\">"
# pattern: start with '>', followed not '<'
	for x in re.findall("(?<="+preptn+")[^<]+", website):
		org.append(x)

	return date, news, newsurl, org

page = 1
URL = "http://www.104.com.tw/area/volunteer/newslist.cfm?page=" + str(page)
#html = getDataFromURL(URL)
#html = getTxtFromFile("result.txt")

# 104news.py is executed by $HOME/www/data/parse.php,
# and parse.php is executed by /usr/bin/crontab,
# so the current path would be located where crontab is.
# That's why it's better to use absolute path.
f = open("/home/fedro/www/database/104news.txt", "w")
for page in range(1, 2):
	URL = "http://www.104.com.tw/area/volunteer/newslist.cfm?page=" + str(page)
	html = getDataFromURL(URL)
	date, news, newsurl, org = parse104(html)
	for x in range(len(date)):
		f.write(date[x]+"\n")		#postdate
		f.write(newsurl[x]+"\n")		#newsurl
		f.write(news[x]+"\n")	#newsname
		f.write(org[x]+"\n")	#org
print "Done! Newslist => 'www/database/104news.txt'"
