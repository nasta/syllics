from django.db import models

import datetime
import random, string

class Log(models.Model):
	action = models.CharField(max_length=20)
	result = models.CharField(max_length=20)
	detail = models.TextField()
	date_time = models.DateTimeField("date_time")

	def __unicode__(self):
		return "%s : %s" % (self.action, self.result)

	def save(self, *args, **kwargs):
		if not self.id:
			self.date_time = datetime.datetime.now()
		return super(Log, self).save(*args, **kwargs)

class Calendar(models.Model):
	url = models.CharField(max_length=6, unique=True)
	class_table = models.TextField()
	content = models.TextField()
	create_date = models.DateTimeField("Date created")
	modified = models.DateTimeField("Last modified")

	def save(self, *args, **kwargs):
		if not self.id:
			self.create_date = datetime.datetime.now()
			self.modified = self.create_date
			self.url = ''.join(random.sample(string.ascii_letters+string.digits, 6))
		self.modified = datetime.datetime.now()
		return super(Calendar, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.url