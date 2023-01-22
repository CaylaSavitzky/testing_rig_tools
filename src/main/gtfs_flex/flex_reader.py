# /Users/caylasavitzky/Downloads/chadroncitytransit-ne-us--flex-v2/stop_times.txt

import pandas
import json
from flex_models import *
from utilities import *


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


def processLocationGroups(data,dao):
	stops = dao.stops
	for dataForStop in data:
		stop = stops.get(str(dataForStop["location_group_id"]))
		if(stop==None):
			stop = Stop(dataForStop,dao)
			stops[stop.myId] = stop
		substopId = dataForStop['location_id']
		if(substopId!=None):
			substop = stops.get(substopId)
			if(substop==None):
				raise Exception("location group ",self.myId," requires substop ",self.location_id)
			else:
				print('adding substop ',substopId,' to stop ',stop.myId, '<',stop,'>')
				stop.substops[substopId] = substop
				print(stop.myId,' has ', len(stop.substops), ' substops')

def readFlexData(folder):
	dao = Dao()
	addData(readJsonToDicts(folder,"locations.geojson"),Stop,dao.stops,dao)
	processLocationGroups(readTxtToDicts(folder,"location_groups.txt"),dao)
	addData(readTxtToDicts(folder,"stops.txt"),Stop,dao.stops,dao)

	# for stop in dao.stops:
	# 	print(stop, dao.stops[stop], dao.stops[stop].substops)


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
