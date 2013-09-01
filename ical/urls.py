from django.conf.urls import patterns, url
from ical import views

urlpatterns = patterns('', 
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name="login"), 
    url(r'^logout$', views.logout, name="logout"), 
    url(r'^(?P<url>[A-Za-z0-9]{6})(.ics|.ICS)?$', views.ical, name="ical"),
)
