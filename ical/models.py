from django.db import models
import datetime

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

class Login(models.Model):
	username = models.CharField(max_length="12", primary_key=True)
	password = models.CharField(max_length="20")


class Calendar(models.Model):
	url = models.CharField(max_length=6, primary_key=True)
	class_table = models.TextField()
	content = models.TextField()
	create_date = models.DateTimeField("date created")

	@classmethod

	def create(self, content=""):
		import random, string
		url = ''.join(random.sample(string.ascii_letters+string.digits, 8))
		return Calendar(url=url, content=content)

	def save(self, *args, **kwargs):
		if not self.id:
			self.date_time = datetime.datetime.now()
		return super(Calendar, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.url