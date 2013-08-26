from django.conf.urls import patterns, url
from ical import views

urlpatterns = patterns('', 
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name="login"), 
    url(r'^(?P<ical_id>[A-Za-z0-9]{8})$', views.ical, name="ical"),
    url(r'^(?P<ical_id>[A-Za-z0-9]{8})[.](ics|ICS)$', views.ical, name="ical"),
)
