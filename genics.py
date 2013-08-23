#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import icalendar
import pytz
from datetime import datetime, timedelta

class Syllics():
    def __init__(self, name):
        self.name = name
        self.cal = icalendar.Calendar()
        self.cal.add('PRODID', '-//SYLLABUS//nasta//CN')
        self.cal.add('VERSION', '2.0')

    def addEvent(self, uid, subject, datetime, place, beforealert, desc):
        event = icalendar.Event()
        event.add('CLASS', 'PUBLIC')
        event.add('CREATED', datetime.now())
        event.add('LAST-MODIFIED', datetime.now())
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
        self.cal.add_component(event)

    def close(self):
        f = open(self.name, 'wb')
        f.write(self.cal.to_ical())


if __name__ == '__main__':
    ics = Syllics('test.ics')
    ics.addEvent('uid1', 'subject1', datetime(2013, 8, 23, 16, 40, 0,
            tzinfo=pytz.timezone('Asia/Shanghai')), 'place1', 1, 'desc')
    ics.addEvent('uid2', 'subject2', datetime(2013, 8, 23, 17, 14, 0,
            tzinfo=pytz.timezone('Asia/Shanghai')), 'place2', 30, 'desc')
    ics.close()
