#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Last Modified: 2013/08/16 19:10
# 课程表获取
# 返回一个包含所有课程信息的List

from  BeautifulSoup import BeautifulSoup

def getClassList(content):
    soup = BeautifulSoup(content)
    i = 0
    result = []
    for tr in soup.table.findAll('tr'):
        if str(tr).find('colspan') != -1:
            break
        lesson = []
        for td in tr.findAll('td'):
            if str(td).find('#f6f6f6">') == -1:
                place = False
            else:
                place = True
            time = False
            try:
                if td['width'] == '300':
                    time = True
            except:
                pass
            texts = td.findAll(text=True)
            if time:
                p = []
                for i in range(len(texts)):
                    p.append(texts[i].strip())
                lesson.append(p)
            elif place:
                texts = " ".join([text.strip() for text in texts])
                lesson.append(texts.split())
            else:
                texts = " ".join([text.strip() for text in texts])
                lesson.append(texts)
        i += 1
        result.append(lesson)
    return result[1:]

if __name__ == '__main__':
    result = getClassList(open('syllabus.htm').read().decode('gbk'))
    for i in result:
        print i
    print len(result)
