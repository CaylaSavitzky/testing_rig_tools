"""
author caylasavitzky


takes a dao and creates map
intended to only process the dao data into a form that is prep for the visualizing tool
"""

from visualize_geo import *
from dao_printer import *
from datetime import datetime;


class DaoVisualizer:

	def __init__(self,x=42.825182,y=-103.000766, zoom=10,showMousePosition=True):
		self.m = folium.Map(location=[x,y], zoom_start=zoom)
		if(showMousePosition):
			enableShowMousePosition(self.m)

	def generateMapFromDao(self,dao,colors=['blue','red'],includeLegend=True):
		if(includeLegend):
			self.addMergedLegend(dao)
		agencyItt = 0
		for agencyId in dao.getAgencies():
			agency=dao.getGtfsObject(Agency,agencyId)
			if(agency==None or dao.getTripsForAgency(agency)==None):
				continue
			color = colors[agencyItt%len(colors)]
			debug.print("using color {}, for agency {}".format(color,agency))
			style = {'fillColor': color, 'lineColor': color}
			layer = self.generateLayerForAgency(agency,style,dao)
			agencyItt+=1
		folium.LayerControl().add_to(self.m)


			
	def addMergedLegend(self,dao):
		legendText = '<span style="font-size:18px">Date created: {}</span> \n\n'.format(datetime.now().strftime("%m/%d/%Y"))
		for agencyId in dao.getAgencies():
			agency=dao.getGtfsObject(Agency,agencyId)
			if(agency==None or dao.getTripsForAgency(agency)==None):
				continue
			debug.print("prepping legend for agency: {}".format(agency.readable))
			legendText += '<span style="font-size:24px">Agency: {}</span> \n\n'.format(agency.readable)
			legendText+="\n".join(getTravelInfoForTripsOfAgencyStrings(dao,agency)).replace("<","&lt;").replace(">","&gt;")
			legendText+="\n\n\n\n"
		addLegend(legendText,self.m)

	def generateLayerForAgency(self,agency,style,dao,printLines=False):
		folium_layer = folium.FeatureGroup(name = agency.readable).add_to(self.m)
		stops = set()
		for trip in dao.getTripsForAgency(agency):
			trip = dao.getGtfsObject(Trip,trip)
			# stopsForStopTimes = list()
			for stop_time in trip.stop_times:
				debug.print("stoptime is {}".format(stop_time))
				stop_time = dao.getGtfsObject(StopTime,stop_time)
				debug.print("stoptime is {}".format(stop_time))
				DaoVisualizer.addStopsToSet(stop_time.stop,stops)
				# stopsForStopTimes.extend(
				# 	DaoVisualizer.getStopsForStopTime(
				# 		trip.stop_times[stop_time],
				# 		style,
				# 		agency.readable,
				# 		folium_layer))
			# debug.print(['stops for stoptimes: ',stopsForStopTimes])
			# if(printLines):
			# 	self.addLinesToMap(stopsForStopTimes,folium_layer)
		DaoVisualizer.addStopsToMap(stops,style,agency.getReadable(),folium_layer)
		return folium_layer


	def save(self,output_folder):
		print("print saving map!")
		self.m.save(output_folder)

	def addStopsToSet(stop,stops : set, depth = 1):
		if(depth>50):
			raise Exception("max stack depth exceeded searching for {}".format(stop.getId().getValue()))
		if(stop.getType()==0):
			stops.add(stop)
		elif(stop.getType()==1):
			for substopId in stop.substops:
				substop = stop.substops[substopId]
				debug.print("recursing to add substop {} from stop {}".format(substop,stop))
				DaoVisualizer.addStopsToSet(substop,stops,depth=depth+1)
		else:
			stops.add(stop)

	def addStopsToMap(stops,style,readableAgencyName, folium_map):
		for stop in stops:
			if(stop.getType()==0):
				DaoVisualizer.addClassicStopToMap(stop,style,readableAgencyName,folium_map)
			elif(stop.getType()==2):
				DaoVisualizer.addLocationToMap(stop,style,readableAgencyName,folium_map)
			else:
				raise Exception("location_groups shouldnot reach this method")
				addStopsToMap(stop.substops)


	# def getStopsForStopTime():
	# 	stops = list()
	# 	st = stop_time
	# 	stop = st.stop
	# 	if(stop.getType()==0):
	# 		DaoVisualizer.addClassicStopToMap(stop,style,readableAgencyName,folium_map)
	# 	elif(stop.getType()==1):
	# 		debug.print(['stop ',stop.getId().getId(),' is a location group with ', len(stop.substops), ' substops'])
	# 		for substop in st.stop.substops:
	# 			stop = st.stop.substops[substop]
	# 			DaoVisualizer.addLocationToMap(stop,style,readableAgencyName,folium_map)
	# 	else:
	# 		DaoVisualizer.addLocationToMap(stop,style,readableAgencyName,folium_map,)
	# 	return stop_time.stop.getCenter()

	def getStopCenterListAndAddStopsToMap(stop_time, style,readableAgencyName, folium_map):
		stops = list()
		st = stop_time
		stop = st.stop
		debug.print(['adding stoptime <',st.getId().getId(),'>  and stop <', str(st.stop.getId().getId()),'> of type: ', str(st.stop.getType())])
		if(stop.getType()==0):
			DaoVisualizer.addClassicStopToMap(stop,style,readableAgencyName,folium_map)
		elif(stop.getType()==1):
			debug.print(['stop ',stop.getId().getId(),' is a location group with ', len(stop.substops), ' substops'])
			for substopId in st.stop.substops:
				stop = st.stop.substops[substopId]
				DaoVisualizer.addLocationToMap(stop,style,readableAgencyName,folium_map)
		else:
			DaoVisualizer.addLocationToMap(stop,style,readableAgencyName,folium_map,)
		return stop_time.stop.getCenter()
		
	def addLinesToMap(self,locationsForStopTimes,folium_map):
		polyLineCords= list()
		baseCords = list()
		for stop_time_locations in locationsForStopTimes:
			cordsForThisStopTime = list()
			for cord in stop_time_locations:
				# debug.print("cord in stop_time_locations")
				if(cord not in cordsForThisStopTime):
					# debug.print("cord not in cordsForThisStopTime")
					for baseCord in baseCords:
						connectAToBOnMap([baseCord,cord],folium_map)
					if(not cord in baseCords):
						# debug.print("not cord in baseCords")
						cordsForThisStopTime.append(cord)
			# debug.print(cordsForThisStopTime)
			baseCords.extend(cordsForThisStopTime)
			# debug.print(baseCords)

	def addLocationToMap(location,style,readableAgencyName,folium_map):
		debug.print(['adding location(stop) to map: ',location.getId().getId()])
		addMarkerWithPopup(
			location.getCenter()[0],
			'location: {}{}'.format(readableAgencyName,
				location.getId().getValue()),
			folium_map)
		debug.print("adding location to map: {}".format(location.getId().getValue()))
		addGeoJsonToMapWithChild(location.initial_data["geometry"],folium_map,style)

	def addClassicStopToMap(stop,style,readableAgencyName,folium_map):
		debug.print(['adding stop to map: ',stop.getId().getId()])
		addMarkerWithPopup(
			stop.getCenter()[0],
			'stop: {}{}'.format(readableAgencyName,
				stop.getId().getValue()),
			folium_map)
		addCircleToMap(stop.getCenter()[0],style,folium_map)


	def getMap(self):
		return self.m



overflowStyle = {"overflow":"scroll"}