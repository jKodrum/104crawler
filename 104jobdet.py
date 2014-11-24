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
		# remove html tag, space character, and statements begin with '#'
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
title = [ "更新:", "工作內容:", "待遇:", "性質:", "地點:", "時段:", "休假:", "上班:", "人數:", "身份:", "經歷:", "學歷:", "學科:", "語文:", "擅長:", "技能:", "其他:", "聯絡人:", "Email:", "親洽:", "電洽:", "其它:" ]
patterns = [ "(?<=更新日期：)[\d-]+", "(?<=工作內容\n).*", "(?<=工作待遇：\n).*", "(?<=工作性質：\n).*", "(?<=上班地點：\n).*", "(?<=上班時段：\n).*", "(?<=休假制度：\n).*", "(?<=可上班日：\n).*", "(?<=需求人數：\n).*", "(?<=接受身份：\n).*", "(?<=工作經歷：\n).*", "(?<=學歷要求：\n).*", "(?<=科系要求：\n).*", "(?<=語文條件：\n).*", "(?<=擅長工具：\n).*", "(?<=工作技能：\n).*", "(?<=其他條件：\n).*", "(?<=聯&nbsp;絡&nbsp;人：\n).*", "(?<=E-mail：\n).*", "(?<=親　　洽：\n).*", "(?<=電　　洽：\n).*?", "(?<=其　　他：).*"]

essence=""
for i in data:
	for j in re.split("\n",i):
		# delete blank lines
		if len(j)>0:
			#print "j: " + j
			'''
			for k in range(len(title)):
				m = re.search(patterns[k], j)
				if m:
					essence += '\n'
					break
					'''
			essence += (j+"\n")

#print "essence***" + essence + "\nessence***"
for i in range(len(title)):
	match = re.search(patterns[i], essence)
	print title[i],
	if match:
		print match.group(0)
	else:
		print 
