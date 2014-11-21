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
essence=""
#cnt=1
for i in data:
	#print cnt
	for j in re.split("\n",i):
		# delete blank lines
		if len(j)>0:
			essence += (j+'\n')
	#cnt+=1
'''
'''
#print essence
print "更新:" + re.search("(?<=更新日期：).*", essence).group(0)
print "工作:" + re.search("(?<=工作內容\n).*", essence).group(0)
print "待遇:" + re.search("(?<=工作待遇：\n).*", essence).group(0)
print "地點:" + re.search("(?<=上班地點：\n).*", essence).group(0)
print "時段:" + re.search("(?<=上班時段：\n).*", essence).group(0)
print "休假:" + re.search("(?<=休假制度：\n).*", essence).group(0)
print "上班:" + re.search("(?<=可上班日：\n).*", essence).group(0)
print "人數:" + re.search("(?<=需求人數：\n).*", essence).group(0)
print "身份:" + re.search("(?<=接受身份：\n).*", essence).group(0)
print "學歷:" + re.search("(?<=學歷要求：\n).*", essence).group(0)
print "學科:" + re.search("(?<=科系要求：\n).*", essence).group(0)
print "語文:" + re.search("(?<=語文條件：\n).*", essence).group(0)
print "擅長:" + re.search("(?<=擅長工具：\n).*", essence).group(0)
print "技能:" + re.search("(?<=工作技能：\n).*", essence).group(0)
print "其他:" + re.search("(?<=其他條件：\n).*", essence).group(0)
