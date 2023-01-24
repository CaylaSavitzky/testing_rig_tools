"""
Mishmash of utilities that it seemed odd to keep in one place
"""


def addManyToManyRelationship(obj,attr,dao,containerType=None,removeId=True,raiseException=True):
	relatedObj = getRelatedObject(obj,attr,dao,containerType)
	attr = removeIdIfTrue(attr,removeId)
	relatedObj.getOrMakeDictForAttr(newattr or attr)[obj.getId]=obj
	obj.getOrMakeDictForAttr(attr)[relatedObj.getId]=relatedObj

def addOneToManyRelationship(obj,attr,dao,containerType=None,removeId=True,raiseException=True):
	relatedObj = getRelatedObject(obj,attr,dao,containerType)
	attr = removeIdIfTrue(attr,removeId)
	relatedObj.getOrMakeDictForAttr(attr)[obj.getId]=obj
	setattr(obj,attr,relatedObj)

def addOneToOneRelationship(obj,attr,dao,containerType=None,removeId=True,raiseException=True):
	relatedObj = getRelatedObject(obj,attr,dao,containerType)
	attr = removeIdIfTrue(attr,removeId)
	setattr(obj,attr,relatedObj)
	setattr(relatedObj,attr,obj)


def removeIdIfTrue(attr,removeId):
	if(removeId):
		attr=attr.replace("_id","")
	return attr

def getRelatedObject(obj,attr,dao,containerType=None,raiseException=False):
	if(containerType==None):
		containerType = type(obj)
	if(hasattr(obj,attr)):
		if(str(getattr(obj,attr))!="nan"):
			container = dao.getContainer(containerType)
			if(container==None):
				raise Exception("no container of type: {} in dao".format(containerType))
			relatedObj = container.get(getattr(obj,attr))
			if(relatedObj==None and raiseException):
				raise Exception("{} {} {} claims to have associated {} {} but none could be found".format(type(self),self,self.myId,containerType,getattr(self,attr)))
			return relatedObj

		

def isNotNullOrNan(val):
	if(val!=None):
		if(str(val)!="nan"):
			return True
	return False

