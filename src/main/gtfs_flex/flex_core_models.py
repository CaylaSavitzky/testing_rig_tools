from abc import ABC, abstractmethod

class Cord(list):
	def __init__(self, *args, **kwargs):
		list.__init__(self, args[0])


class GtfsObjId:
	def __init__(self, agency: str, myId : str):
		self.agency = agency
		self.myId = myId
	def getAgency(self):
		return self.agency
	def getId(self):
		return self.myId;
	def getValue(self):
		return '{}--{}'.format(self.agency,self.myId)
	def __eq__(self, obj):
		return isinstance(obj,GtfsObjId) and obj.getAgency()==self.getAgency() and obj.getId()==self.getId()
	def __hash__(self):
		return ((self.getAgency() or "None").__hash__() + 31*(self.getId() or None).__hash__())



'''
base for all other gtfs models
'''
class GtfsObject:
	def getId(self):
		return myId

	def setId(self, agency: str, myId : str):
		self.myId = "{}---{}".format(agency,myId)

	def setId(self, myId : GtfsObjId):
		self.myId = myId

	@abstractmethod
	def __init__(self, initial_data,agency,dao):
		pass
	def getOrMakeDictForAttr(self,attr):
		if(not hasattr(self,"attrDicts")):
			self.attrDicts = dict()
		if(self.attrDicts.get(attr)==None):
			self.attrDicts[attr] = dict()
		return self.attrDicts.get(attr)
	def putDictForAttr(self,attr,dictForAttr):
		if(not hasattr(self,"attrDicts")):
			self.attrDicts = dict()
		if(not self.attrDicts.get(attr)==None):
			raise Exception("will not overwrite dict -- {}. dict already exists and has {} entries".format(attr,len(self.attrDicts.get(attr))))
		self.attrDicts[attr]=dictForAttr



class Dao:
	def __contains__(self,item):
		raise Exception("use getDict instead")
		if(not type(item) in self.data):
			return False
		if(not item in self.data.get(type(item))):
			return False
		return True
	@abstractmethod
	def getGtfsObject(self,objType,id):
		pass
	@abstractmethod
	def addGftsObject(self,obj):
		pass
	@abstractmethod
	def getTrips(self):
		pass
	@abstractmethod
	def getStops(self):
		pass
	@abstractmethod
	def getStopTimes(self):
		pass
	@abstractmethod
	def getAgencyName(self):
		pass
	@abstractmethod
	def readFlexDirectory(self):
		pass
	@abstractmethod
	def getContainer(self,objType):
		pass
