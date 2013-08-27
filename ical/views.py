from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from ical.models import Calendar, Login

from syllabus import getClassList, getClassTable

def index(request):
    return render(request, "index.html")

def login(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		table = getClassTable(username, password)
		if table:
			result = getClassList(table)
			return HttpResponse(result)
		else:
			return HttpResponse(u"login failed")
	else:
		return HttpResponse("login")

def ical(request, ical_id):
    ics = get_object_or_404(Calendar, pk=ical_id)
    response = HttpResponse(ics.content)
    response['content-type']='text/calendar'
    return response
