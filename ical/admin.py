from django.contrib import admin
from ical.models import Calendar, Log

class LogAdmin(admin.ModelAdmin):
	fields = ['action', 'result', 'detail', 'date_time']
	list_display = ('date_time', 'action', 'result')
	list_filter = ['date_time', 'action']

class CalendarAdmin(admin.ModelAdmin):
	list_display = ('url', 'create_date')
	list_filter = ['create_date']

admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Log, LogAdmin)
