#!/usr/bin/env python
# -*- coding: utf-8 -*-

def printCourse(course):
	print """course_num: %s
course_name: %s
teacher: %s
dayofweek: %d
weeks: %s
place: %s
time: %s
""" % (course.course_num, course.course_name, course.teacher, course.dayofweek, course.weeks, course.place, course.time)


def test_Course():
	from genics import Course

	courseTable = open("E:/Desktop/newtable.html").read().decode("gbk")
	for i in Course.genCourse(courseTable):
		printCourse(i)

def test_Syllics():
	from genics import Course, Syllics
	course = Course("num", "name", "teacher", [1, 3, 5], 1, "place", "1-2")
	ics = Syllics()
	ics.addCourse(course)
	ics.save("E:/Desktop/test.ics")

def test():
	from genics import Course, Syllics
	courseTable = open("E:/Desktop/newtable.html").read().decode("gbk")
	ics = Syllics(courseTable)
	ics.save("E:/Desktop/test.ics")

if __name__ == "__main__":
	#test_Course()
	#test_Syllics()
	test()
