#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
import icalendar
import pytz

from datetime import datetime, timedelta
from BeautifulSoup import BeautifulSoup


# 2013年秋季学期开始
_termdate = datetime(2013, 9, 2)

################################################
#
#   上课时间表
#   每一行是一节课
#   第一个元组是开始的时间，第二个元组是结束时间
#
################################################
_timeTable = (
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


class Course():
    """
        Course(course_num, course_name, teacher, weeks, dayofweek, place, time)
    """

    def __init__(self, course_num, course_name, teacher, weeks, dayofweek, place, time):
        self.course_num  =  course_num
        self.course_name =  course_name
        self.teacher     =  teacher
        self.dayofweek   =  dayofweek
        self.weeks       =  weeks
        self.place       =  place
        self.time        =  time

    @classmethod
    def genCourse(cls, courseTable):
        """
            genCourse(courseTable)
        """
        soup   = BeautifulSoup(courseTable)
        names  = []
        classList = []

        count = 0
        for tr in soup.table.findAll('tr'):
            if str(tr).find('colspan') != -1:
                continue
            i = 0
            lesson = {}
            for td in tr.findAll('td'):
                texts = td.findAll(text=True)
                texts = " ".join([text.strip() for text in texts])
                if count == 0:
                    names.append(texts)
                else:
                    lesson[names[i]] = texts
                i += 1
            if count != 0:
                classList.append(lesson)
            count += 1

        # 遍历课程列表
        for cs in classList:
            course_num  = cs[u"课程号"]
            course_name = cs[u"课程名称"]
            teacher     = cs[u"上课教师"]
            place       = cs[u"上课地点"]

            dayofweek = int(cs[u"上课星期"].split(u"星期")[1])

            m = re.compile(r".(\d{1,2})\-(\d{1,2}).+").match(cs[u"上课节次"]).groups()
            time = "-".join(m)

            weeks = []
            for i in cs[u"上课周次"].split(','):
                m = re.compile(r"(\d+)\-(\d+).\(?(.)?\)?").match(i)
                beginweek, endweek, numbers = m.groups()
                beginweek, endweek = int(beginweek), int(endweek)
                if not numbers:
                    step = 1
                else:
                    step = 2
                weeks += range(beginweek, endweek+1, step)

            yield Course(course_num, course_name, teacher, weeks, dayofweek, place, time)


class Syllics():
    """
        Syllics类，可根据课程上课信息生成ics文件
    """
    def __init__(self):
        self.cal = icalendar.Calendar()
        self.cal.add('PRODID', '-//nasta//SYLLABUS//CN')
        self.cal.add('VERSION', '2.0')
        self.cal.add('X-WR-CALNAME', '课程表')
        self.cal.add('CALSCALE', 'GREGORIAN')

    def addCourse(self, course):
        desc = u"教师: %s" % course.teacher
        beforealert = 30
        time = [int(i) for i in course.time.split("-")]
        print course.dayofweek

        for week_num in course.weeks:
            uid = "%s|%s|%d|%d" % (course.course_num, course.course_name,
                    week_num, course.dayofweek)
            starttime = timedelta(weeks = week_num - 1, days = course.dayofweek - 1, 
                    hours = _timeTable[time[0]] [0][0],
                    minutes = _timeTable[time[0]] [0][1]) + _termdate

            endtime = timedelta(weeks = week_num - 1, days = course.dayofweek - 1, 
                    hours = _timeTable[time[1]] [1][0],
                    minutes = _timeTable[time[1]] [1][1]) + _termdate

            #print course.course_name, starttime, endtime, course.place, uid, desc, beforealert
            self.addEvent(subject=course.course_name, starttime=starttime, endtime=endtime, 
                        place=course.place, uid=uid, desc=desc, beforealert=beforealert)


    def addEvent(self, subject, starttime, endtime, place, uid, desc="", beforealert=0):
        """
            addEvent(self, subject, starttime, endtime, place, uid, desc="", beforealert=0):

        """

        # 添加Event
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

        # 添加Alarm
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
        """
        """
        return self.cal.to_ical()