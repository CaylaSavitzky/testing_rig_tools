"""
Mishmash of utilities that it seemed odd to keep in one place
"""

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

def readTxtToDicts(folder,filename):
	# turn first row plus row into an obj for stops
	# dict(zip(a,b))
	try:
		return pandas.read_csv(folder+'/'+filename).to_dict(orient='records')
	except FileNotFoundError:
		print("could not read file: "+ folder+'/'+filename)
		return None

def readJsonToDicts(folder,filename):
	try:
		return json.load(open(folder+'/'+filename))['features']
	except FileNotFoundError:
		print("could not read file: "+ folder+'/'+filename)
		return None