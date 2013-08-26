#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import BeautifulSoup, re
import traceback
import loginfo

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

	s = requests.Session()
	r = s.get(_INDEX_URL)
	if r.content.find("loginURL:'userPasswordValidate.portal'") == -1:
		from logerr import logerr
		logerr(u"获得首页", u"不符合预期", r.content)
		return None

	r = s.post(_POST_URL, data=param)
	print r.content
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

if __name__ == "__main__":
	print getClassTable("a", "b")
	print getClassTable(loginfo.USER, loginfo.PASS)