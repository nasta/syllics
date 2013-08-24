#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import icalendar
import pytz
from datetime import datetime, timedelta

class Syllics():
    def __init__(self, name):
        self.name = name
        self.cal = icalendar.Calendar()
        self.cal.add('PRODID', '-//nasta//SYLLABUS//CN')
        self.cal.add('VERSION', '2.0')
        self.cal.add('X-WR-CALNAME', '课程表')
        self.cal.add('CALSCALE', 'GREGORIAN')

    def addEvent(self, subject, time, place, beforealert, desc, week):
        uid = "%s|%s|%d" % (self.name, subject, week)
        event = icalendar.Event()
        event.add('CREATED', datetime.now())
        event.add('LAST-MODIFIED', datetime.now())
        event.add('DESCRIPTION', desc)
        event.add('DTEND', time)
        event.add('DTSTAMP', time)
        event.add('DTSTART', time)
        event.add('LOCATION', place)
        event.add('PRIORITY', '5')
        event.add('SUMMARY', subject)
        event.add('UID', uid)
        alarm = icalendar.Alarm()
        alarm.add('TRIGGER', timedelta(seconds=-60*beforealert))
        alarm.add('ACTION', 'DISPLAY')
        alarm.add('DESCRIPTION', 'Reminder')
        event.add_component(alarm)
        self.cal.add_component(event)

    def ical(self):
        return self.cal.to_ical()

def test():
    ics = Syllics('test')
    for i in range(1000):
        ics.addEvent('subject2', datetime(2013, 8, 23, 17, 14, 0), 'place2', 30, 'desc', i)
    ics.ical()

if __name__ == '__main__':
    from timeit import Timer 
    t1 = Timer("test()", "from __main__ import test")
    print t1.timeit(10)
    print t1.repeat(3, 10)