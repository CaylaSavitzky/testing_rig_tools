"""
models for flex classes.
add more as needed.
"""

from utilities import *
from abc import ABC, abstractmethod

class GtfsObject:
	@abstractmethod
	def getId(self):
		pass

class BookingRuleId(GtfsObject):
	possibleIds = ["booking_rule_id"]
	def __init__(self, initial_data,dao):
		self.trips = dict()
		for key in initial_data:
			datum = initial_data[key]
			setattr(self,key,datum)
			if (key in self.possibleIds):
				self.myId = datum
	def getId(self):
		return self.myId
	

class Trip(GtfsObject):
	possibleIds = ["trip_id"]
	def __init__(self, initial_data,dao):
		self.stop_times = dict()
		# print("creating trip from " + str(initial_data))
		for key in initial_data:
			datum = initial_data[key]
			if (key in self.possibleIds):
				self.myId = datum
			if (key == "stop_id"):
				self.stop=dao.stops[datum]
				if (self.stop==None):
					raise Exception("could not find stop " + datum)
			setattr(self,key,datum)
		# self.route=dao.routes.get(self.route_id)
		# # print(dao.routes.get(self.route_id))
		# if (self.route==None):
		# 	print("could not find route " + self.route_id)
		# 	raise Exception("trips must have route")
		# self.route.trips[self.myId]=self
	def getId(self):
		return self.myId
	

class StopTime(GtfsObject):
	possibleIds = ["backup_id"]
	def __init__(self, initial_data,dao):		
		for key in initial_data:
			datum = initial_data[key]
			setattr(self,key,datum)
			if (key in self.possibleIds):
				self.myId = datum
		self.stop_id = str(self.stop_id)
		self.stop=dao.stops.get(self.stop_id)
		if (self.stop==None):
			print("could not find stop " + str(self.stop_id))
			raise Exception("stop_times must have stop")
		self.trip=dao.trips.get(self.trip_id)
		if (self.trip==None):
			print("could not find trip " + self.trip_id)
			raise Exception("stop_times must have trip")
		self.trip.stop_times[self.stop_sequence]=self
		# print("\n\n")
		# print("StopTime: ", self.myId, " tripId ", self.trip_id, "Trip tripId ", self.trip.myId)
		# printShortHandTripInfo(self.trip)
		if(isNotNullOrNan(self.pickup_booking_rule_id)):
			self.pickup_booking_rule=dao.bookingRules.get(self.pickup_booking_rule_id)
			if(self.pickup_booking_rule==None):
				raise Exception("Stoptime {} {} claims to have associated pickup booking rule {} but none could be found".format(self,self.myId,self.pickup_booking_rule_id) )
			self.pickup_booking_rule.trips[self.myId]=self
		
		if(isNotNullOrNan(self.drop_off_booking_rule_id)):
			self.drop_off_booking_rule=dao.bookingRules.get(self.drop_off_booking_rule_id)
			if(self.drop_off_booking_rule==None):
				raise Exception("Stoptime {} {} claims to have associated drop_off booking rule {} but none could be found".format(self,self.myId,self.drop_off_booking_rule_id) )
			self.drop_off_booking_rule.trips[self.myId]=self
	def getId(self):
		return self.myId



# somthing that turns core id into ID
class Stop(GtfsObject):
	possibleIds = ["stop_id","location_group_id","id"]
	def __init__(self, initial_data,dao):
		self.substops = dict()
		for key in initial_data:
			if (key in self.possibleIds):
				self.type = self.possibleIds.index(key)
				self.myId = str(initial_data[key])
				# if(self.type==0):
				# 	print(type(self.myId))
				# 	print(self.myId,self)
			setattr(self,key,initial_data[key])
		self.initial_data = initial_data
		self.parentStops = dict()

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
	

class Dao:
	stops = dict()
	stop_times = dict()
	trips = dict()
	bookingRules = dict()
	def getGtfsObject(type,id):
		raise Exception("implement getGtfsObject")

	def getAgencyName(self):
		return 'temp agencyname'


def printShortHandTripInfo(trip):
	out = print("\n",trip.myId, trip)
	for stop_time in trip.stop_times:
		st = trip.stop_times[stop_time]
		print(str(st.myId), str(st.stop.myId))