#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from json import dumps
import requests
import BeautifulSoup, re

_INDEX_URL   = "http://my.tjut.edu.cn/index.portal"
_POST_URL    = "http://my.tjut.edu.cn/userPasswordValidate.portal"
_REQUEST_URL = "http://my.tjut.edu.cn/pnull.portal"
_LOGOUT_URL  = "http://my.tjut.edu.cn/logout.portal"


def getClassTable(username, password):

    param = {
        "Login.Token1" : username,
        "Login.Token2" : password,
        "goto" : "http://my.tjut.edu.cn/loginSuccess.portal",
        "gotoOnFail" : "http://my.tjut.edu.cn/loginFailure.portal"
    }

    # 带状态的requests对象
    session = requests.Session()

    # 判断获取首页内容是否正确
    req = session.get(_INDEX_URL)
    if req.content.find("loginURL:'userPasswordValidate.portal'") == -1:
        raise RuntimeError(u"get url failed")

    # 登陆
    req = session.post(_POST_URL, data=param)
    if req.content.find("false") != -1:
        raise RuntimeError(u"login failed")

    # 获取课程表URL
    req = session.get(_INDEX_URL)
    content = req.content
    soup = BeautifulSoup.BeautifulSoup(content)
    urls = soup.findAll(attrs={'class':re.compile('^lazyLoadUrl$')})

    # TODO
    # 不知道什么原因，urls有时只含有1个URL
    try:
        info_url  = _REQUEST_URL + urls[0].attrMap['url']
        class_url = _REQUEST_URL + urls[1].attrMap['url']

    except IndexError, e:
        # fallback url
        class_url = _REQUEST_URL + "?.p=Znxjb20ud2lzY29tLnBvcnRhbC5zaXRlLnYyLmltcGwuRnJhZ21lbnRXaW5kb3d8ZjcxMHx2aWV3fG5vcm1hbHw_&.nctp=true&.ll=true"

    # 获取课程表
    content = session.get(class_url).content
    soup = BeautifulSoup.BeautifulSoup(content)

    # 提取列表
    table = soup.findAll(attrs={"style":"padding-top:0px;"})
    table = table[1].table

    session.get(_LOGOUT_URL)

    return str(table)

if __name__ == '__main__':
    table = getClassTable("", "")
