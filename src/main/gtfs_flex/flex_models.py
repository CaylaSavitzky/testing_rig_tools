"""
models for flex classes.
add more as needed.
"""

from utilities import *
from flex_core_models import *

class Agency(GtfsObject):
	def __init__(self, initial_data,agencies,dao):
		contentList = list()
		for key in initial_data:
			datum = initial_data[key]
			setattr(self,key,datum)
			contentList.append(str(datum))
		self.setId(GtfsObjId(self.agency_id,"".join(contentList).__hash__()))
		agencies[self.getId()]=self.getId()
		self.readable = self.agency_id
		if(hasattr(self,"agency_name")):
			self.readable = self.agency_name

class BookingRule(GtfsObject):
	possibleIds = ["booking_rule_id"]
	def __init__(self, initial_data,agencies,dao):
		self.trips = dict()
		super().__init__(initial_data,agencies,dao)
	def getId(self):
		return self.myId
	

class Trip(GtfsObject):
	possibleIds = ["trip_id"]
	def __init__(self, initial_data,agencies,dao):
		self.stop_times = dict()
		self.putDictForAttr("trip",self.stop_times)
		# print("creating trip from " + str(initial_data))
		super().__init__(initial_data,agencies,dao)
		# print(dir(self))
		# self.stop=dao.getGtfsObject(Stop,self.stop_id)
		# if (self.stop==None):
		# 	raise Exception("could not find stop " + datum)
	def getId(self):
		return self.myId
	

class StopTime(GtfsObject):
	possibleIds = ["backup_id"]
	def __init__(self, initial_data,agencies,dao):		
		super().__init__(initial_data,agencies,dao)
		self.stop_id = str(self.stop_id)
		addOneToManyRelationship(self,"stop_id",dao,Stop)
		addOneToManyRelationship(self,"trip_id",dao,Trip)
		# print("\n\n")
		# print("StopTime: ", self.myId, " tripId ", self.trip_id, "Trip tripId ", self.trip.myId)
		# printShortHandTripInfo(self.trip)
		if(isNotNullOrNan(self.pickup_booking_rule_id)):
			addOneToManyRelationship(self,"pickup_booking_rule_id",dao,BookingRule)
		if(isNotNullOrNan(self.drop_off_booking_rule_id)):
			addOneToManyRelationship(self,"drop_off_booking_rule_id",dao,BookingRule)
	def getId(self):
		return self.myId



# somthing that turns core id into ID
class Stop(GtfsObject):
	xNum=0
	yNum=1
	possibleIds = ["stop_id","location_group_id","id"]
	def __init__(self, initial_data,agencies,dao):
		super().__init__(initial_data,agencies,dao)
		self.initial_data = initial_data
		self.substops = dict()
		self.putDictForAttr("substops",self.substops)
		self.parentStops = dict()
		self.putDictForAttr("parentStops",self.parentStops)
		self.type = self.possibleIds.index(self.idKey)

	def getType(self):
		return self.type

	def getBoundingBox(self):
		if(hasattr(self,"boundingBox")):
			return self.boundingBox
		#if switch to geojson replace this with better built in method
		if(self.type==0):
			raise Exception("boundingBox not implemented for regular stops")
		if(self.type==1):
			raise Exception("boundingBox not implemented for locationgroups")
		else:

			xmin = self.initial_data["geometry"]["coordinates"][0][0][self.xNum]
			xmax = xmin
			ymin = self.initial_data["geometry"]["coordinates"][0][0][self.yNum]
			ymax = ymin
			for cord in self.initial_data["geometry"]["coordinates"][0]:
				x=cord[self.xNum]
				if(x<xmin):
					xmin=x
				if(x>xmax):
					xmax=x
				y=cord[self.yNum]
				if(y<ymin):
					ymin=y
				if(y>ymax):
					ymax=y
			self.xmin = xmin
			self.xmax = xmax
			self.ymin = ymin
			self.ymax = ymax
			self.boundingBox=[[self.xmin,self.ymin],[self.xmax,self.ymax]]
			return self.boundingBox

	def getCenter(self):
		out = list()
		if(self.type==0):
			out.append([self.stop_lat,self.stop_lon])
		elif(self.type==1):
			for substop in self.substops:
				out.append(self.substops[substop].getCenter())
		else:
			#if switch to geojson replace this with better built in method
			bB = self.getBoundingBox()
			# print("for stop:{} using boundingBox: {}".format(self.getId().getId(),bB))
			invertedCord = [
			((bB[1][self.yNum]+bB[0][self.yNum])/2),
			((bB[1][self.xNum]+bB[0][self.xNum])/2)]
			# print("adding cord: {}".format(invertedCord))
			out.append(invertedCord)
		return out
	def getId(self):
		return self.myId
	


class DaoImpl:
	data={
	Agency:dict(),
	Stop:dict(),
	StopTime:dict(),
	Trip:dict(),
	BookingRule:dict(),
	}
	def __contains__(self,item):
		if(not type(item) in self.data):
			return False
		if(not item in self.data.get(type(item))):
			return False
		return True
	def getGtfsObject(self,objType,gtfsId):
		if(not objType in self.data):
			raise Exception("dao cannot process objects of type {}".format(objType))
		return self.data.get(objType).get(gtfsId)
	# def getGtfsObject(self,objType,agency,objId):
	# 	if(not objType in self.data):
	# 		raise Exception("dao cannot process objects of type {}".format(objType))
	# 	return self.data.get(objType).get(GtfsObjId(agency,objId))
	def addGftsObject(self,obj):
		if(not type(obj) in self.data):
			raise Exception("dao cannot process objects of type {}".format(type(obj)))
		if(type(obj)==Trip):
			agency = obj.getId().getAgency()
			typeHolder =self.data.get(type(obj))
			typeAgencyHolder = typeHolder.get(agency) 
			if(typeAgencyHolder==None):
				typeAgencyHolder = dict()
				typeHolder[agency]=typeAgencyHolder
			# print("adding trip {} to agency {}".format(obj.getId().getValue(),agency.getId()))
			typeAgencyHolder[obj.getId()]=obj
		self.data.get(type(obj))[obj.getId()] = obj
	def getDict(self,clazz):
		raise Exception("implement getDict")
	def getTrips(self):
		raise Exception("implement getTrips as merged dict using | operator")
		return self.data[Trip]
	def getStops(self):
		return self.data[Stop]
	def getStopTimes(self):
		return self.data[StopTime]
	def getAgencies(self):
		return self.data[Agency]
	def getTripsForAgency(self,agency):
		# print(self.data[Trip])
		# print(agency)
		return self.data[Trip].get(agency)
	def getContainer(self,objType):
		return self.data.get(objType)





def printShortHandTripInfo(trip):
	out = print("\n",trip.myId, trip)
	for stop_time in trip.stop_times:
		st = trip.stop_times[stop_time]
		print(str(st.myId), str(st.stop.myId))