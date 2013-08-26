#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from json import dumps
from BeautifulSoup import BeautifulSoup

def getClassList(content):
    soup   = BeautifulSoup(content)
    names  = []
    result = []

    count = 0
    for tr in soup.table.findAll('tr'):
        if str(tr).find('colspan') != -1:
            continue
        i = 0
        lesson = {}
        for td in tr.findAll('td'):
            texts = td.findAll(text=True)
            texts = " ".join([text.strip() for text in texts])
            if count == 0:
                names.append(texts)
            else:
                lesson[names[i]] = texts
            i += 1
        if count != 0:
            result.append(lesson)
        count += 1
    return result

if __name__ == '__main__':
    import mytjut, loginfo
    table = mytjut.getClassTable(loginfo.USER, loginfo.PASS)
    result = getClassList(table)
    for i in result:
        for key in i.keys():
            print "%s : %s" % (key, i[key])
        print ""