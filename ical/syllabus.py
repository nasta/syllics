#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from json import dumps
import requests
import BeautifulSoup, re
import traceback
import loginfo

def getClassList(content):
    soup   = BeautifulSoup.BeautifulSoup(content)
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

def getClassTable(username, password):
    _INDEX_URL   = "http://my.tjut.edu.cn/index.portal"
    _POST_URL    = "http://my.tjut.edu.cn/userPasswordValidate.portal"
    _REQUEST_URL = "http://my.tjut.edu.cn/pnull.portal"
    _LOGOUT_URL  = "http://my.tjut.edu.cn/logout.portal"
    param = {
        "Login.Token1" : username,
        "Login.Token2" : password,
        "goto" : "http://my.tjut.edu.cn/loginSuccess.portal",
        "gotoOnFail" : "http://my.tjut.edu.cn/loginFailure.portal"
    }

    s = requests.Session()
    r = s.get(_INDEX_URL)
    if r.content.find("loginURL:'userPasswordValidate.portal'") == -1:
        from logerr import logerr
        logerr(u"获得首页", u"不符合预期", r.content)
        return None

    r = s.post(_POST_URL, data=param)
    if r.content.find("false") != -1:
        from logerr import logerr
        logerr(u"登陆", u"登录失败", r.content)
        return False

    r = s.get(_INDEX_URL)
    content = r.content
    soup = BeautifulSoup.BeautifulSoup(content)
    urls = soup.findAll(attrs={'class':re.compile('^lazyLoadUrl$')})
    try:
        info_url  = _REQUEST_URL + urls[0].attrMap['url']
        class_url = _REQUEST_URL + urls[1].attrMap['url']
    except IndexError, e:
        class_url = _REQUEST_URL + "?.p=Znxjb20ud2lzY29tLnBvcnRhbC5zaXRlLnYyLmltcGwuRnJhZ21lbnRXaW5kb3d8ZjcxMHx2aWV3fG5vcm1hbHw_&.nctp=true&.ll=true"

    content = s.get(class_url).content
    soup = BeautifulSoup.BeautifulSoup(content)
    table = soup.findAll(attrs={"style":"padding-top:0px;"})
    table = table[1].table
    s.get(_LOGOUT_URL)
    return str(table)

if __name__ == '__main__':
    import mytjut, loginfo
    table = mytjut.getClassTable(loginfo.USER, loginfo.PASS)
    result = getClassList(table)
    for i in result:
        for key in i.keys():
            print "%s : %s" % (key, i[key])
        print ""

    print getClassTable("a", "b")
    print getClassTable(loginfo.USER, loginfo.PASS)