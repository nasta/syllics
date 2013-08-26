from ical.models import Log

def logerr(action, result, detail=""):
	log = Log(action, result, detail)
	log.save()