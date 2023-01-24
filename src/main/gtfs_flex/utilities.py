"""
Mishmash of utilities that it seemed odd to keep in one place
"""


def addManyToManyRelationship(obj,attr,dao,containerType=None):
	relatedObj = addManytoMeRelationship(obj,attr,dao,containerType)
	obj.getOrMakeDictForAttr(attr)[relatedObj.getId]=relatedObj

def addOneToManyRelationship(obj,attr,dao,containerType=None,raiseException=False):
	relatedObj = addManytoMeRelationship(obj,attr,dao,containerType)
	if(relatedObj==None and raiseException):
		raise Exception("{} {} {} claims to have associated {} {} but none could be found".format(type(self),self,self.myId,containerType,getattr(self,attr)))
	# print("object: {}; attr: {}; relatedObj: {}".format(obj,attr,relatedObj))
	setattr(obj,attr,relatedObj)

def addOneToOneRelationship(obj,attr,dao,containerType=None):
	relatedObj = getRelatedObject(obj,attr,dao,containerType)
	setattr(obj,attr,relatedObj)
	setattr(relatedObj,attr,obj)


def addManytoMeRelationship(obj,attr,dao,containerType=None):
	relatedObj = getRelatedObject(obj,attr,dao,containerType)
	relatedObj.getOrMakeDictForAttr(attr)[obj.getId]=obj
	return relatedObj

def addOneToMeRelationship(obj,attr,dao,containerType=None):
	relatedObj = getRelatedObject(obj,attr,dao,containerType)
	setattr(relatedObj,attr,obj)
	return relatedObj

def getRelatedObject(obj,attr,dao,containerType=None):
	if(containerType==None):
		containerType = type(obj)
	if(hasattr(obj,attr)):
		if(str(getattr(obj,attr))!="nan"):
			container = dao.getContainer(containerType)
			if(container==None):
				raise Exception("no container of type: {} in dao".format(containerType))
			return container.get(getattr(obj,attr))

		

def isNotNullOrNan(val):
	if(val!=None):
		if(str(val)!="nan"):
			return True
	return False

