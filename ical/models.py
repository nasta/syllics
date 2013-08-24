from django.db import models

class Calendar(models.Model):
	url = models.CharField(max_length=8, primary_key=True)
	content = models.TextField()
	create_date = models.DateTimeField("date created", auto_now=True)

	@classmethod
	def create(self, content=""):
		import random, string
		url = ''.join(random.sample(string.ascii_letters+string.digits, 8))
		return Calendar(url=url, content=content)

	def __unicode__(self):
		return self.url