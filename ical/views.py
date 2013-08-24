from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from ical.models import Calendar

def index(request):
    return HttpResponse("index")

def ical(request, ical_id):
    ics = get_object_or_404(Calendar, pk=ical_id)
    response = HttpResponse(ics.content)
    response['content-type']='text/calendar'
    return response
