from ical.models import Log


def logerr(action, result, detail=""):
	log = Log(action=action, result=result, detail=detail)
	log.save()
