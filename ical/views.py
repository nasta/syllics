from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from ical.models import Calendar, Log

from ics import getClassTable, Syllics

def index(request):
    return render(request, "index.html")

def login(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		try:
			table = getClassTable(username, password)
		except RuntimeError, e:
			Log(action=u"getCourseTable", result=e).save()
			return HttpResponse(u"login failed")
		cal = Calendar(class_table=table, content=Syllics(table).ical())
		cal.save()
		url = "/ical/" + cal.url
		return redirect(url)
	else:
		return HttpResponse("login")

def ical(request, url):
    ics = get_object_or_404(Calendar, url=url)
    response = HttpResponse(ics.content)
    response["content-type"]  = "text/calendar; charset=utf-8"
    response["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return response
