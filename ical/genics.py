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
    _termdate = datetime(2013, 9, 2)
    ics = Syllics()
    for cs in classList:
        course_num = cs[u"课程号"]
        course_name = cs[u"课程名称"]
        teacher = cs[u"上课教师"]
        weeks = []
        dayofweek = int(cs[u"上课星期"].split(u"星期")[1])
        m = re.compile(r".(\d{1,2})\-(\d{1,2}).+").match(cs[u"上课节次"])
        beginclass, endclass = [int(i) for i in m.groups()]
        for i in cs[u"上课周次"].split(','):
            m = re.compile(r"(\d+)\-(\d+).\(?(.)?\)?").match(i)
            beginweek, endweek, numbers = m.groups()
            beginweek, endweek = int(beginweek), int(endweek)
            if not numbers:
                step = 1
            else:
                step = 2
            weeks += range(beginweek, endweek+1, step)

        place = cs[u"上课地点"]

        for week in weeks:
            uid = "%s|%s|%d|%d" % (course_num, course_name, week, dayofweek)
            starttime = timedelta(weeks=week-1, days=dayofweek-1, 
                hours=timeTable[beginclass][0][0],
                minutes=timeTable[beginclass][0][1]) + _termdate
            endtime = timedelta(weeks=week-1, days=dayofweek-1, 
                hours=timeTable[endclass][1][0],
                minutes=timeTable[endclass][1][1]) + _termdate
            ics.addEvent(course_name, starttime, endtime, place, 30, teacher, uid)
    ics.save("b.ics")
    return ics.ical()

class Syllics():
    def __init__(self):
        self.cal = icalendar.Calendar()
        self.cal.add('PRODID', '-//nasta//SYLLABUS//CN')
        self.cal.add('VERSION', '2.0')
        self.cal.add('X-WR-CALNAME', '课程表')
        self.cal.add('CALSCALE', 'GREGORIAN')

    def addEvent(self, subject, starttime, endtime, place, beforealert, desc, uid):
        event = icalendar.Event()
        event.add('CREATED', datetime.now())
        event.add('LAST-MODIFIED', datetime.now())
        event.add('DESCRIPTION', desc)
        event.add('DTEND', endtime)
        event.add('DTSTAMP', starttime)
        event.add('DTSTART', starttime)
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

    def save(self, name):
        f = open(name, "wb")
        f.write(self.cal.to_ical())
        f.close()

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
        ics = genClassSchedule(result)
        f = open("test.ics", "w")
        f.write(ics)
        f.close()
    else:
        print "getClassTable failed"