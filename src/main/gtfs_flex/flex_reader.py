# /Users/caylasavitzky/Downloads/chadroncitytransit-ne-us--flex-v2/stop_times.txt

import pandas
import json
from FlexModels import *

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

def readFlexData(folder):
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

	return dao
