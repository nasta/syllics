#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
import icalendar
import pytz
from datetime import datetime, timedelta

timeTable = (
    None,
    ((8, 0), (8, 45)),
    ((8, 55), (9, 40)),
    ((10, 10), (10, 55)),
    ((11, 05), (11, 50)),
    ((12, 20), (13, 40)),
    ((12, 20), (13, 40)),
    ((14, 0), (14, 45)),
    ((14, 55), (15, 40)),
    ((16, 10), (16, 55)),
    ((17, 05), (17, 50)),
    ((18, 30), (19, 15)),
    ((19, 25), (20, 10)),
    ((20, 20), (21, 05)),
)


def genClassSchedule(classList):
    for cs in classList:
        cs[u"课程号"]
        cs[u"课程名称"]
        cs[u"上课教师"]
        dayofweek = cs[u"上课星期"].split(u"星期")[1]
        m = re.compile(r".(\d{1,2})\-(\d{1,2}).+").match(cs[u"上课节次"])
        beginclass, endclass = [int(i) for i in m.groups()]
        m = re.compile(r"(\d+)\-(\d+).\(?(.)?\)?").match(cs[u"上课周次"])
        beginweek, endweek, numbers = m.groups()
        beginweek = int(beginweek)
        endweek = int(endweek)
        if numbers == u"双":
            numbers = "even"
        elif numbers == u"单":
            numbers = "odd"
        else:
            numbers = None
        print beginclass, endclass
        cs[u"上课地点"]


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
    """
    from timeit import Timer 
    t1 = Timer("test()", "from __main__ import test")
    print t1.timeit(10)
    print t1.repeat(3, 10)
    """
    from loginfo import USER, PASS
    from syllabus import getClassList, getClassTable
    table = getClassTable(USER, PASS)
    if table:
        result = getClassList(open("E:/Desktop/newtable.html").read().decode("gbk"))
        print genClassSchedule(result)
    else:
        print "getClassTable failed"