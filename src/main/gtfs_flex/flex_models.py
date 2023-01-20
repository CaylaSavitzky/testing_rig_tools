class BookingRuleId:
	possibleIds = ["booking_rule_id"]
	def __init__(self, initial_data,dao):
		self.trips = dict()
		for key in initial_data:
			datum = initial_data[key]
			setattr(self,key,datum)
			if (key in self.possibleIds):
				self.myId = datum
	

class Trip:
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
	

class StopTime:
	possibleIds = ["backup_id"]
	def __init__(self, initial_data,dao):		
		for key in initial_data:
			datum = initial_data[key]
			setattr(self,key,datum)
			if (key in self.possibleIds):
				self.myId = datum
		self.stop_id = str(self.stop_id)
		self.stop=dao.stops.get(self.stop_id)
		i = self.stop_id
		i2 = 4148390
		if(i!=i2):
			print(False, ": type of stop_id = ", type(self.stop_id))
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
		self.pickup_booking_rule=dao.bookingRules.get(self.pickup_booking_rule_id)
		self.pickup_booking_rule.trips[self.myId]=self
		self.drop_off_booking_rule=dao.bookingRules.get(self.drop_off_booking_rule_id)
		self.drop_off_booking_rule.trips[self.myId]=self



# somthing that turns core id into ID
class Stop:
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

	def getCenter(self):
		out = list()
		if(self.type==0):
			raise Exception("getCenter not implemented for regular stops")
			out.append(self.lat,self.lon)
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
	

class Dao:
	stops = dict()
	stop_times = dict()
	trips = dict()
	bookingRules = dict()
	def getAgencyName(self):
		return 'temp agencyname'


def printShortHandTripInfo(trip):
	out = print("\n",trip.myId, trip)
	for stop_time in trip.stop_times:
		st = trip.stop_times[stop_time]
		print(str(st.myId), str(st.stop.myId))