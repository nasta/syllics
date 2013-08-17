#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import icalendar
import pytz
from datetime import datetime

class ics():
    def __init__(self, name):
        self.cal = icalendar.Calendar()
        self.cal.add('PRODID', '-//SYLLABUS//nasta//CN')
        self.cal.add('VERSION', '2.0')

    def addEvent(self, uid, subject, datetime, place, beforealert, desc):
        event = icalendar.Event()
        event.add('CLASS', 'PUBLIC')
        event.add('DESCRIPTION', desc)
        event.add('DTEND', datetime)
        event.add('DTSTAMP', datetime)
        event.add('DTSTART', datetime)
        event.add('LOCATION', place)
        event.add('PRIORITY', '5')
        event.add('SUMMARY', subject)
        event.add('UID', uid)
        alarm = icalendar.Alarm()
        alarm.add('TRIGGER', timedelta(seconds=-60*beforealert))
        alarm.add('ACTION', 'DISPLAY')
        alarm.add('DESCRIPTION', 'Reminder')
        event.add_component(alarm)

    def close(self):
        f=open(name, 'wb')
        f.write(self.cal.to_ical())

