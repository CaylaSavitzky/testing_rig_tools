"""
author caylasavitzky

reads in flex data from an unzipped flex file
"""
import pandas
import json
from flex_models import *
from utilities import *



def readTxtToDicts(folder,filename):
	# turn first row plus row into an obj for stops
	# dict(zip(a,b))
	try:
		return pandas.read_csv(folder+'/'+filename,converters={'stop_id': str}).to_dict(orient='records')
	except FileNotFoundError:
		debug.print("could not read file: "+ folder+'/'+filename)
		return None

def readJsonToDicts(folder,filename):
	try:
		return json.load(open(folder+'/'+filename))['features']
	except FileNotFoundError:
		debug.print("could not read file: "+ folder+'/'+filename)
		return None

class FlexReader():
	def extractAgencyData(data,dao):
		extractedData=dict() #should be a set but sooo much refactoring
		if(data==None):
			raise Exception("no agencies read from agencies.txt")
		itt = 0
		for datum in data:
			datum["file_itt"] = itt
			datum = Agency(datum,dao)
			extractedData[datum]=datum
			debug.print("in flex reader: {}".format(datum.getId()))
			if(datum in dao):
				debug.print(dataHolder.get(datum.getId()).__dict__)
				debug.print(datum.__dict__)
				raise Exception("datum ids and equivilents must be unique");
			dao.addGftsObject(datum)
			itt += 1
		return extractedData

	def addData(data,clazz,agency,dao):
		if(data==None):
			return
		# todo: check if a datum is a subgroup of another stop and vice versa?
		itt = 0
		for datum in data:
			datum["file_itt"] = itt
			datum = clazz(datum,agency,dao)
			debug.print("in flex reader: {}".format(datum.getId().getValue()))
			if(datum in dao):
				debug.print(dataHolder.get(datum.getId()).__dict__)
				debug.print(datum.__dict__)
				raise Exception("datum ids and equivilents must be unique");
			dao.addGftsObject(datum)
			itt += 1


	def processLocationGroups(data,agency,dao):
		if(data==None):
			return
		stops = dao.getStops()
		for dataForStop in data:
			stop = stops.get(GtfsObjId(list(agency.values())[0],str(dataForStop["location_group_id"])))
			if(stop==None):
				stop = Stop(dataForStop,agency,dao)
				print(stop.getId())
				stops[stop.getId()] = stop
			substopId = dataForStop['location_id']
			if(substopId!=None):
				substop = dao.getGtfsObject(Stop,GtfsObjId(stop.getId().getAgency(),str(substopId)))
				if(substop==None):
					raise Exception("location group ",stop.getId().getValue()," requires substop ",stop.location_id)
				else:
					# debug.print('adding substop ',substopId,' to stop ',stop.getId(), '<',stop,'>')
					if(type(substop)!=Stop):
						raise Exception("stop {}'s substop {} must be of type Stop".format(stop,substop))
					stop.substops[substopId] = substop
					substop.parentStops[stop.getId()]=stop
					print(stop.getId(),' has ', len(stop.substops), ' substops')
		len(dao.getStops())


	def readFlexDirectoryIntoDao(folder,dao):
		print("reading gtfs from {}".format(folder))
		agencies = FlexReader.extractAgencyData(readTxtToDicts(folder,"agency.txt"),dao)
		debug.print(agencies)
		FlexReader.addData(readJsonToDicts(folder,"locations.geojson"),Stop,agencies,dao)
		FlexReader.addData(readTxtToDicts(folder,"stops.txt"),Stop,agencies,dao)
		FlexReader.processLocationGroups(readTxtToDicts(folder,"location_groups.txt"),agencies,dao)
		# for stop in dao.getStops():
		# 	debug.print(stop, dao.getStops()[stop], dao.getStops()[stop].substops)
		FlexReader.addData(readTxtToDicts(folder,"booking_rules.txt"),BookingRule,agencies,dao)
		FlexReader.addData(readTxtToDicts(folder,"calendar_dates.txt"),ServiceSchedule,agencies,dao)
		FlexReader.addData(readTxtToDicts(folder,"calendar.txt"),ServiceSchedule,agencies,dao)
		# for service in dao.getServiceIds():
		# 	debug.print("printing service id: {}".format(service))
		# for route in dao.routes:
		# 	debug.print(route, dao.routes[route])
		FlexReader.addData(readTxtToDicts(folder,"trips.txt"),Trip,agencies,dao)
		# for trip in dao.getTrips():
		# 	debug.print(trip, dao.getTrips()[trip])
		FlexReader.addData(readTxtToDicts(folder,"stop_times.txt"),StopTime,agencies,dao)
		# for stoptime in dao.stop_times:
		# 	debug.print(stoptime, dao.stop_times[stoptime].stop.getId())



