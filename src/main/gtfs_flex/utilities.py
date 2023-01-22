def addRelationship(obj,attr,dao):
	if(hasattr(obj,attr)):
		if(str(getattr(obj,attr))!="nan"):
			# get class of object, add method of dao to get list for class or maybe if
			# all objects juse were in one dict (ugh, performance issues probs aren't 
			# relevant at this scale), you could look by unique id or something
			raise Exception("finish coding addRelationship()")
	

def isNotNullOrNan(val):
	if(val!=None):
		if(str(val)!="nan"):
			return True
	return False