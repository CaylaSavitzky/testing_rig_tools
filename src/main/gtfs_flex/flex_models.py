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
		agencies[self.agency_id]=self.agency_id

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
	possibleIds = ["stop_id","location_group_id","id"]
	def __init__(self, initial_data,agencies,dao):
		super().__init__(initial_data,agencies,dao)
		self.initial_data = initial_data
		self.substops = dict()
		self.putDictForAttr("substops",self.substops)
		self.parentStops = dict()
		self.putDictForAttr("parentStops",self.parentStops)

	def getCenter(self):
		out = list()
		if(self.type==0):
			out.append([self.stop_lat,self.stop_lon])
		elif(self.type==1):
			for substop in self.substops:
				out.append(self.substops[substop].getCenter())
		else:
			print("fix Stop getCenter")
			# change to run through points to get min&max x,y and calc center
			firstCord = self.initial_data["geometry"]["coordinates"][0][0]
			invertedCord = [firstCord[1],firstCord[0]]
			print(firstCord)
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
	BookingRule:dict()
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
		self.data.get(type(obj))[obj.getId()] = obj
	def getDict(self,clazz):
		raise Exception("implement getDict")
	def getTrips(self):
		return self.data[Trip]
	def getStops(self):
		return self.data[Stop]
	def getStopTimes(self):
		return self.data[stop_times]
	def getContainer(self,objType):
		return self.data.get(objType)




def printShortHandTripInfo(trip):
	out = print("\n",trip.myId, trip)
	for stop_time in trip.stop_times:
		st = trip.stop_times[stop_time]
		print(str(st.myId), str(st.stop.myId))