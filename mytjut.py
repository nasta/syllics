#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import BeautifulSoup
import re

import loginfo

INDEX_URL = "http://my.tjut.edu.cn/index.portal"
POST_URL = "http://my.tjut.edu.cn/userPasswordValidate.portal"
REQUEST_URL = "http://my.tjut.edu.cn/pnull.portal"
PARAM = {
	"Login.Token1" : loginfo.USER,
	"Login.Token2" : loginfo.PASS,
	"goto" : "http://my.tjut.edu.cn/loginSuccess.portal",
	"gotoOnFail" : "http://my.tjut.edu.cn/loginFailure.portal"
}
headers = {
	"User-Agent" : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0",
	"Referer" : "http://my.tjut.edu.cn/index.portal",
	"Content-Type" : "application/x-www-form-urlencoded",
	"Connection" : "keep-alive"
}

s = requests.Session()
r = s.get(INDEX_URL)
r = s.post(POST_URL, data=PARAM)
r = s.get(INDEX_URL)
content = r.content
soup = BeautifulSoup.BeautifulSoup(content)
urls = soup.findAll(attrs={'class':re.compile('^lazyLoadUrl$')})
info_url  = REQUEST_URL + urls[0].attrMap['url']
class_url = REQUEST_URL + urls[1].attrMap['url']
s.get(info_url).content
content = s.get(class_url).content
soup = BeautifulSoup.BeautifulSoup(content)
table = soup.findAll(attrs={"style":"padding-top:0px;"})
table = table[1].table

if __name__ == "__main__":
	print table