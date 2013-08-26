from django.db import models

class Login(models.Model):
	username = models.CharField(max_length="12", primary_key=True)
	password = models.CharField(max_length="20")

class Calendar(models.Model):
	url = models.CharField(max_length=6, primary_key=True)
	class_table = models.TextField()
	content = models.TextField()
	create_date = models.DateTimeField("date created", auto_now=True)

	@classmethod
	def create(self, content=""):
		import random, string
		url = ''.join(random.sample(string.ascii_letters+string.digits, 8))
		return Calendar(url=url, content=content)

	def __unicode__(self):
		return self.url

class Log(models.Model):
	action = models.CharField(max_length=20)
	result = models.CharField(max_length=20)
	detail = models.TextField()
	date_time = models.DateTimeField("Date", auto_now=True)

	def __unicode__(self):
		return "%s : %s" % (self.action, self.result)