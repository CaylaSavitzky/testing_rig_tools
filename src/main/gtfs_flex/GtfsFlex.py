# /Users/caylasavitzky/Downloads/chadroncitytransit-ne-us--flex-v2/stop_times.txt

import pandas
import sys
import json




# class ServiceId:
# 	def __init__(self, initial_data):
# 		for key in initial_data:
# 			setattr(self, key, initial_data[key])


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
		
		self.stop=dao.stops.get(self.stop_id)
		if (self.stop==None):
			print("could not find stop " + self.stop_id)
			raise Exception("stop_times must have stop")
		# print("StopTime: ", self.myId, " stopId ", self.stop_id, "stop stopId ", self.stop.myId)

		self.trip=dao.trips.get(self.trip_id)
		if (self.trip==None):
			print("could not find trip " + self.trip_id)
			raise Exception("stop_times must have trip")
		self.trip.stop_times[self.stop_sequence]=self
		print("\n\n")
		print("StopTime: ", self.myId, " tripId ", self.trip_id, "Trip tripId ", self.trip.myId)
		printShortHandTripInfo(self.trip)
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
				self.myId = initial_data[key]
			setattr(self,key,initial_data[key])
	

class Dao:
	stops = dict()
	stop_times = dict()
	trips = dict()
	bookingRules = dict()


def readTxtToDicts(folder,filename):
	# turn first row plus row into an obj for stops
	# dict(zip(a,b))
	return pandas.read_csv(folder+'/'+filename).to_dict(orient='records')

def readJsonToDicts(folder,filename):
	return json.load(open(folder+'/'+filename))['features']

def addData(data, clazz,dataHolder,dao):
	# todo: check if a datum is a subgroup of another stop and vice versa?
	itt = 0
	for datum in data:
		datum["backup_id"] = itt
		datum = clazz(datum,dao)
		if(dataHolder.get(datum.myId)!=None):
			print(dataHolder.get(datum.myId).__dict__)
			print(datum.__dict__)
			raise Exception("datum ids and equivilents must be unique");
		dataHolder[datum.myId] = datum
		itt += 1


def add_location_groups_stops(data,dao):
	stops = dao.stops
	# todo: this should just be part of Stop
	for dataForStop in data:
		stop = stops.get(dataForStop["location_group_id"])
		if(stop==None):
			stop = Stop(dataForStop,dao)
			stops[stop.myId] = stop
		substopId = dataForStop['location_id']
		if(substopId!=None):
			substop = stops.get(substopId)
			stop.substops[substopId] = substop

def stringifyBookingInfo(rule):
	out = ""
	if(rule.booking_type==2):
		out += " by booking at most " + str(rule.prior_notice_start_day) + " days ago at " + str(rule.prior_notice_start_time)
		out += " and at least "+str(rule.prior_notice_last_day) +" days ago at " + str(rule.prior_notice_last_time)
	else:
		out += " by booking at least " + str(rule.prior_notice_duration_min) +" minutes ago "
	if(rule.booking_type==1):
		out += " and at most " + str(rule.prior_notice_duration_max) + " minutes ago"
	return out;

def stringifyStopTimeOutput(st):
	out = ""
	# out +="in stop_time " + str(st.myId)
	out += "location " + str(st.stop.myId)
	out += " between " + str(st.start_pickup_drop_off_window)
	out += " and " + str(st.end_pickup_drop_off_window)
	out += stringifyBookingInfo(st.pickup_booking_rule)
	return out


def getTravelInfoForTripsStrings(dao):
	outputStringsContainer = list()
	for trip in dao.trips:
		out = "for "+trip + ": \n"
		itt = 0
		trip = dao.trips[trip]
		for stop_time in trip.stop_times:
			if(itt<len(trip.stop_times)-1):
				if(itt>0):
					out += " or \n"
				out += "travel from: "
			if(itt==len(trip.stop_times)-1):
				out += 'to: ' 
			out += stringifyStopTimeOutput(trip.stop_times[stop_time])
			out +="\n"
			itt+=1
		outputStringsContainer.append(out)
	return outputStringsContainer


def printShortHandTripInfo(trip):
	out = print("\n",trip.myId, trip)
	for stop_time in trip.stop_times:
		st = trip.stop_times[stop_time]
		print(str(st.myId), str(st.stop.myId))





folder = sys.argv[1]

dao = Dao()

addData(readJsonToDicts(folder,"locations.geojson"),Stop,dao.stops,dao)
add_location_groups_stops(readTxtToDicts(folder,"location_groups.txt"),dao)
addData(readTxtToDicts(folder,"stops.txt"),Stop,dao.stops,dao)

# for stop in dao.stops:
# 	print(stop, dao.stops[stop])


addData(readTxtToDicts(folder,"booking_rules.txt"),BookingRuleId,dao.bookingRules,dao)

# for route in dao.routes:
# 	print(route, dao.routes[route])


addData(readTxtToDicts(folder,"trips.txt"),Trip,dao.trips,dao)

# for trip in dao.trips:
# 	print(trip, dao.trips[trip])

addData(readTxtToDicts(folder,"stop_times.txt"),StopTime,dao.stop_times,dao)

# for stoptime in dao.stop_times:
# 	print(stoptime, dao.stop_times[stoptime].stop.myId)


# for trip in dao.trips:
# 	out = print("\n",trip, dao.trips[trip])
# 	for stop_time in dao.trips[trip].stop_times:
# 		st = dao.trips[trip].stop_times[stop_time]
# 		print(str(st.myId), str(st.stop.myId))

for out in getTravelInfoForTripsStrings(dao):
	print(out+"\n")