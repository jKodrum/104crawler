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
    return data



if len(sys.argv)!=2:
    print "agrv Error."
    print "[usage]: python [inputHtml]"
    sys.exit(0)

infile = sys.argv[1]
htmlfile = getTxtFromFile(infile)
data = parse104(htmlfile)

# "detail" is a list of [engtitle, zhtitle, repattern, matchedstr]
detail = [ [ "update", "更新:" , "(?<=更新日期：)[\d-]+" ],
        [ "content", "工作內容:", "(?<=工作內容\n).*" ],
        [ "treatment", "工作待遇:", "(?<=工作待遇：\n).*" ],
        [ "type", "工作性質:", "(?<=工作性質：\n).*" ],
        [ "location", "上班地點:", "(?<=上班地點：\n).*" ],
        [ "worktime", "上班時段:", "(?<=上班時段：\n).*" ],
        [ "leavesys", "休假制度:", "(?<=休假制度：\n).*" ],
        [ "availability", "可上班日:", "(?<=可上班日：\n).*" ],
        [ "reqnum", "需求人數:", "(?<=需求人數：\n).*" ],
        [ "acceptid", "接受身份:", "(?<=接受身份：\n).*" ],
        [ "exp", "工作經歷:", "(?<=工作經歷：\n).*" ],
        [ "education", "學歷要求:", "(?<=學歷要求：\n).*" ],
        [ "department", "科系要求:", "(?<=科系要求：\n).*" ],
        [ "language", "語文條件:", "(?<=語文條件：\n).*" ],
        [ "tool", "擅長工具:", "(?<=擅長工具：\n).*" ],
        [ "skill", "工作技能:", "(?<=工作技能：\n).*" ],
        [ "othercond", "其他條件:", "(?<=其他條件：\n).*" ],
        [ "contact", "聯絡人:", "(?<=聯&nbsp;絡&nbsp;人：\n).*" ],
        [ "emailsrc", "Email:", "(?<=E-mail：\nfun_flash_output\(\")[^\"]+" ],
        [ "inperson", "親洽:", "(?<=親　　洽：\n).*" ],
        [ "telesrc", "電洽:", "(?<=電　　洽：).*\n.*" ],
        [ "other", "其它:", "(?<=其　　他：).*" ]]

essence=""
for i in data:
    for j in re.split("\n",i):
        # ignore blank lines
        if len(j)>0:
            essence += (j+"\n")

for i in range(len(detail)):
    if "telesrc" in detail[i][0]:
        # the telephone numbers src is a link to an image which show tele numbers.
        teletmp = re.search(detail[i][2], htmlfile)
        if teletmp:
            match = re.search("(?<=src=')[^']+", teletmp.group(0))
    elif "emailsrc" in detail[i][0]:
        # the email src is a link to a flash called by "fun_flash_output"
        match = re.search(detail[i][2], essence)
    else:
        match = re.search(detail[i][2], essence)

    if match:
        detail[i].append(match.group(0))
    else:
        detail[i].append('')

for i in range(len(detail)):
    for j in [1,3]:
        print detail[i][j],
    print
