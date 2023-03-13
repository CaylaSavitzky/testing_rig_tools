"""
author Cayla Savitzky

the core bits and parts that the flex models implement and work with
"""

from abc import ABC, abstractmethod

class Cord(list):
	def __init__(self, *args, **kwargs):
		list.__init__(self, args[0])


class Agency():
	def __init__(self, initial_data,dao):
		contentList = list()
		for key in initial_data:
			datum = initial_data[key]
			setattr(self,key,datum)
			contentList.append(str(datum))
		self.readable=""
		if(hasattr(self,"agency_id")):
			self.readable = self.agency_id
		if(hasattr(self,"agency_name")):
			self.readable = self.agency_name
		self.setId("".join(contentList).__hash__())
	def getId(self):
		return self.myId
	def setId(self, myId:int):
		self.myId = myId
	def getReadable(self):
		return self.readable


class GtfsObjId:
	def __init__(self, agency: Agency, myId : str):
		self.agency = agency
		self.myId = myId
	def getAgency(self):
		return self.agency
	def getId(self):
		return self.myId;
	def getValue(self):
		return '{}--{}'.format(self.agency.getReadable(),self.myId)
	def __eq__(self, obj):
		return isinstance(obj,GtfsObjId) and obj.getAgency()==self.getAgency() and obj.getId()==self.getId()
	def __hash__(self):
		return ((self.getAgency() or "None").__hash__() + 31*(self.getId() or None).__hash__())
	def __str__(self):
		return "{}-{}".format(self.getValue(),self.__hash__())



'''
base for all other gtfs models
'''
class GtfsObject:
	def __str__(self):
		return "{} with id {} and hash {}".format(type(self),str(self.getId()),self.__hash__())

	def getId(self):
		return self.myId

	def setId(self, myId : GtfsObjId):
		self.myId = myId

	def __init__(self, initial_data,agencies,dao):
		for key in initial_data:
			datum = initial_data[key]
			setattr(self,key,str(datum))
			if (key in self.possibleIds):
				self.tmpId = str(datum)
				self.idKey = key
		if(not hasattr(self,"tmpId")):
			print("{} has these attr: {}".format(self,dir(self)))
			raise Exception("cannot find id for {} itt: {} from list of options: {} ".format(
				type(self),self.file_itt,self.possibleIds))
		self.setId(GtfsObjId(GtfsObject.getAgencyFromAgencies(agencies),self.tmpId))

	def getAgencyFromAgencies(agencies):
		if(len(agencies)==1):
			return list(agencies.values())[0]
		elif(len(agencies)==0):
			raise Exception("no agencies in gtfs")
			# setattr(self,key,self.tmpId)
		else:
			raise Exception("multiple agencies in gtfs")
		# print("loading agency: {}".format(self.getId().getAgency()))
			

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
	def getAgencies(self):
		pass
	@abstractmethod
	def readFlexDirectory(self):
		pass
	@abstractmethod
	def getTripsForAgency(self,agency):
		pass
	@abstractmethod
	def getContainer(self,objType):
		pass
