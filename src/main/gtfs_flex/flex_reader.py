# /Users/caylasavitzky/Downloads/chadroncitytransit-ne-us--flex-v2/stop_times.txt

import pandas
import json
from flex_models import *
from utilities import *



def readTxtToDicts(folder,filename):
	# turn first row plus row into an obj for stops
	# dict(zip(a,b))
	try:
		return pandas.read_csv(folder+'/'+filename).to_dict(orient='records')
	except FileNotFoundError:
		print("could not read file: "+ folder+'/'+filename)
		return None

def readJsonToDicts(folder,filename):
	try:
		return json.load(open(folder+'/'+filename))['features']
	except FileNotFoundError:
		print("could not read file: "+ folder+'/'+filename)
		return None

class FlexReader():
	def addData(data,clazz,agency,dao):
		if(data==None):
			return
		# todo: check if a datum is a subgroup of another stop and vice versa?
		itt = 0
		for datum in data:
			datum["backup_id"] = itt
			datum = clazz(datum,agency,dao)
			if(datum in dao):
				print(dataHolder.get(datum.getId()).__dict__)
				print(datum.__dict__)
				raise Exception("datum ids and equivilents must be unique");
			dao.addGftsObject(datum)
			itt += 1


	def processLocationGroups(data,agency,dao):
		if(data==None):
			return
		stops = dao.getStops()
		for dataForStop in data:
			stop = stops.get(str(dataForStop["location_group_id"]))
			if(stop==None):
				stop = Stop(dataForStop,agency,dao)
				stops[stop.getId()] = stop
			substopId = dataForStop['location_id']
			if(substopId!=None):
				substop = stops.get(substopId)
				if(substop==None):
					raise Exception("location group ",stop.getId()," requires substop ",stop.location_id)
				else:
					# print('adding substop ',substopId,' to stop ',stop.getId(), '<',stop,'>')
					stop.substops[substopId] = substop
					substop.parentStops[stop.getId()]=stop
					# print(stop.getId(),' has ', len(stop.substops), ' substops')


	def readFlexDirectoryIntoDao(folder,dao, debug=False):
		agency = {"agency":"agency"}
		# FlexReader.addData(readTxtToDicts(folder,"agency.txt"),Agency,agency,dao)

		FlexReader.addData(readJsonToDicts(folder,"locations.geojson"),Stop,agency,dao)
		FlexReader.processLocationGroups(readTxtToDicts(folder,"location_groups.txt"),agency,dao)
		FlexReader.addData(readTxtToDicts(folder,"stops.txt"),Stop,agency,dao)
		# for stop in dao.getStops():
		# 	print(stop, dao.getStops()[stop], dao.getStops()[stop].substops)
		FlexReader.addData(readTxtToDicts(folder,"booking_rules.txt"),BookingRule,agency,dao)
		# for route in dao.routes:
		# 	print(route, dao.routes[route])
		FlexReader.addData(readTxtToDicts(folder,"trips.txt"),Trip,agency,dao)
		# for trip in dao.getTrips():
		# 	print(trip, dao.getTrips()[trip])
		FlexReader.addData(readTxtToDicts(folder,"stop_times.txt"),StopTime,agency,dao)
		# for stoptime in dao.stop_times:
		# 	print(stoptime, dao.stop_times[stoptime].stop.getId())



