# -*- coding: utf-8 -*-
# program: 104jobdet.py
# author: jKodrum
# usage: 
#   $ python 104jobdet.py
#
# purpose:
#   generate INSERT command to insert the extracted data to database
#
# describe:
#   There are two steps of parsing.
#   1. Parse 104 angel volunteer website "http://www.104.com.tw"
#       This is a volunteer-job-integrated website. But I have to link to 
#       another domain of url to get the detail info of a job. So the main
#       idea in the step is to get the urls of all jobs here.
#   2. Dig deep into the urls got from step 1 to get detail info.
#
# output:
#   psql_INSERT, psql_UPDATE, rails_console_INSERT, data columns
#   I use rails_console_INSERT for now.
import sys
import urllib2
import re

# either from url or from file
def getData( source, mode ):
    if mode == "fromurl":
        try:
            response = urllib2.urlopen(urllib2.Request(source))
        except (ValueError, urllib2.URLError) as e:
            print e
            sys.exit(0)
        data = response.read() 
        # remove '\r' character
        data = data.replace('\r', '')
        return data
    else:
        f = open( source, 'r' )
        data = f.read()
        # remove '\r' character
        data = data.replace('\r', '')
        return data


# Parse 104 angel volunteer website "http://www.104.com.tw"
# ==============================================================
# data column: joburl, job, orgurl, url, location
# returned data contains 10 jobs
def parse_angel_104(website):
    base_url = "http://www.104.com.tw"
    # find <td align="left">
    narrowed_html = re.findall("<td align=\"left\">.*", website)
    # pattern: start with 'href="', followed not ' '
    url_ptn = re.compile("(?<=href=\")[^\s]+(?!title)")
    # pattern: start with '>', followed not '<'
    chinese_ptn = re.compile("(?<=>)[^<]+")
    data = []
    for x in narrowed_html:
        if url_ptn.search(x):
            found_url = url_ptn.search(x).group(0)
            data.append(base_url + found_url.replace('"', ''))
        if chinese_ptn.search(x):
            data.append(chinese_ptn.search(x).group(0))
    return data


def get_jobs_url():
    urls = []
    # There are 10 jobs per page
    max_page = 31
    for page in range(1, max_page):
        url = "http://www.104.com.tw/area/volunteer/volunteer.cfm?page=" + str(page)
        raw_html = getData(url, "fromurl")
        ten_jobs = parse_angel_104(raw_html)
        for x in range(len(ten_jobs)/5):
            urls.append(ten_jobs[x*5]+"\n")        #job url
    return urls


# Parse the website got from 104 angel volunteer
# to get more detailed info of a volunteer job
# ==============================================================
# narrow the target range and remove html tags
def narrow_parse(website):
    # match the strings
    # begin with "<div class=\"intro\">" or "<div class=\"interview\">"
    # end with "<div class=\"intro\">" or "<div class=\"interview\">" or "<script type"
    # (?s) means re.DOTALL
    # (?:...) means non-capturing mode
    # (?!...) matches if ... doesn't match. In anothor word, not followed by ...
    narrowed_html = re.findall("(?s)(<div class=\"(?:intro|interview)\">(?:.(?!<script type|<div class=\"(?:intro|interview)))*)", website)
    data = []
    for x in narrowed_html:
        # remove html tag, space character, and statements begin with '#'
        data.append( re.sub("<[^>]*>|[ \t]+|#(?<=#).*","",str(x)) )
    return data


def parse_individule_104_web( url ):
    # "detail" is a list of [engtitle, zhtitle, repattern, matchedstr]
    # It's initialized with first 3 columns.
    # The last 1 columns will be appended in parse_individule_104_web function
    detail = [ [ "last_modified", "更新:" , "(?<=更新日期：)[\d-]+" ],
            [ "title", "志工服務:", "(?<=comp_name\">\s\s\s<h1>)[^<\t]+" ],
            [ "joburl", "服務網址:", "" ],
            [ "content", "工作內容:", "(?<=工作內容\n).*" ],
            [ "treatment", "工作待遇:", "(?<=工作待遇：\n).*" ],
            [ "jobtype", "工作性質:", "(?<=工作性質：\n).*" ],
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
    raw_html = getData(url, "fromurl")
    narrowed_data = narrow_parse(raw_html)
    # convert narrowed_data into string and remove blank lines
    for i in narrowed_data:
        for j in re.split("\n",i):
            # ignore blank lines
            if len(j)>0:
                essence += (j+"\n")

    for i in range(len(detail)):
        if "joburl" in detail[i][0]:
            detail[i].append(url.replace('\n', ''))
            continue
        elif "telesrc" in detail[i][0]:
            # the telephone numbers src is a link to an image which shows tele numbers.
            teletmp = re.search(detail[i][2], raw_html)
            if teletmp:
                match = re.search("(?<=src=')[^']+", teletmp.group(0))
        elif "title" in detail[i][0]:
            match = re.search(detail[i][2], raw_html)
        else:
            match = re.search(detail[i][2], essence)

        if match:
            string = match.group(0)
            if "location" in detail[i][0]:
                string = re.sub("地圖","",string)
            detail[i].append(string)
        else:
            detail[i].append('')
    return detail


# 4 output mode: sql update, sql insert, rails console insert, columns
def output_result(detail, mode=""):
    # generate UPDATE SQL command
    if mode == "sql_update":
        print "UPDATE jobs SET",
        for i in range(1,len(detail)):
            print detail[i][0] + "='" + detail[i][3] + "'",
            if i < len(detail)-1:
                print ",",
        print "WHERE joburl='" + detail[2][3] + "';"
    # generate INSERT SQL command
    elif mode == "sql_insert":
        print "INSERT INTO jobs (",
        for i in range(1,len(detail)):
            print detail[i][0],
            if i < len(detail)-1:
                print ",",
        print ") VALUES(",
        for i in range(1,len(detail)):
            print "'" + detail[i][3] + "'",
            if i < len(detail)-1:
                print ",",
        print ");"
    # generate Rails Console INSERT command
    elif mode == "rails":
        print "Job.create!(",
        for i in range(len(detail)):
            print detail[i][0] + ": '" + detail[i][3] + "'",
            if i < len(detail)-1:
                print ",",
        print ")"
    # columns output
    else:
        for i in range(1,len(detail)):
            for j in [1,3]:
                print detail[i][j],
            print


# main
# ==============================================================
all_job_url = get_jobs_url()
for url in all_job_url:
    result = parse_individule_104_web(url)
    output_result(result, "rails")
