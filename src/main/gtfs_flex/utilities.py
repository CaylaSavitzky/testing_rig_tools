"""
Mishmash of utilities that it seemed odd to keep in one place
"""
from flex_core_models import *

def addManyToManyRelationship(obj,attr,dao,containerType=None,removeId=True,raiseException=True,agency=None):
	relatedObj = getRelatedObject(obj,attr,dao,containerType,raiseException=raiseException,agency=agency)
	attr = removeIdIfTrue(attr,removeId)
	relatedObj.getOrMakeDictForAttr(newattr or attr)[obj.getId()]=obj
	obj.getOrMakeDictForAttr(attr)[relatedObj.getId()]=relatedObj

def addOneToManyRelationship(obj,attr,dao,containerType=None,removeId=True,raiseException=True,agency=None):
	relatedObj = getRelatedObject(obj,attr,dao,containerType,raiseException=raiseException,agency=agency)
	attr = removeIdIfTrue(attr,removeId)
	relatedObj.getOrMakeDictForAttr(attr)[obj.getId()]=obj
	setattr(obj,attr,relatedObj)

def addOneToOneRelationship(obj,attr,dao,containerType=None,removeId=True,raiseException=True,agency=None):
	relatedObj = getRelatedObject(obj,attr,dao,containerType,raiseException=raiseException,agency=agency)
	attr = removeIdIfTrue(attr,removeId)
	setattr(obj,attr,relatedObj)
	setattr(relatedObj,attr,obj)


def removeIdIfTrue(attr,removeId):
	if(removeId):
		attr=attr.replace("_id","")
	return attr

def getRelatedObject(obj,attr,dao,containerType=None,raiseException=False,agency = None):
	agency = agency or obj.getId().getAgency()
	if(containerType==None):
		containerType = type(obj)
	if(hasattr(obj,attr)):
		if(str(getattr(obj,attr))!="nan"):
			container = dao.getContainer(containerType)
			if(container==None):
				raise Exception("no container of type: {} in dao".format(containerType))
			relatedObjId = GtfsObjId(agency,getattr(obj,attr))
			printDebug("looking for: {} {}".format(containerType,relatedObjId))
			relatedObj = dao.getGtfsObject(containerType,relatedObjId)
			if(relatedObj==None and raiseException):
				raise Exception("{} {} {} claims to have associated {} {} {} but none could be found".format(
					type(obj),obj,obj.getId().getValue(),
					containerType,relatedObjId.getValue(),
					str(relatedObjId.getAgency().getAgency())+"---"+str(relatedObjId.getId())))
			return relatedObj

		

def isNotNullOrNan(val):
	if(val!=None):
		if(str(val)!="nan"):
			return True
	return False

debug = True
def printDebug(stuffToPrint):
	if debug == True:
		if(not "__iter__" in dir(stuffToPrint)):
			print(stuffToPrint)
		else:
			print("".join(str(item) for item in stuffToPrint))