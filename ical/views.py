# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from ical.models import Calendar, Log

from ics import getClassTable, Syllics

def index(request):
	request.session["url"] = ""
	return render(request, "index.html")

def logout(request):
	request.session["url"] = ""
	return redirect(login)


def login(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		alarm    = int(request.POST["alarm"])
		try:
			table = getClassTable(username, password)
		except RuntimeError, e:
			Log(action=u"getCourseTable", result=e).save()
			request.session["loginFalse"] = True
			return redirect(login)
		cal = Calendar(class_table=table, content=Syllics(table, alarm).ical())
		saved = False
		while not saved:
			try:
				cal.save()
				saved = True
			except IntegrityError, e:
				pass

		url = "http://" + request.META["HTTP_HOST"] + "/" + cal.url + ".ics"
		request.session['url'] = url
		return redirect(login)
	else:
		context = {}
		if "loginFalse" in request.session:
			if request.session["loginFalse"] == True:
				context["error"] = u"登录失败，请重试"
		request.session["loginFalse"] = "False"

		if 'url' in request.session:
			context["url"] = request.session["url"]
		else:
			context["url"] = ""

		return render(request, "login.html", context)

def ical(request, url):
    ics = get_object_or_404(Calendar, url=url)
    response = HttpResponse(ics.content)
    response["content-type"]  = "text/calendar; charset=utf-8"
    response["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return response