from visualize_geo import *
from flex_cli import *
"""
takes dao and creates map
"""

class DaoVisualizer:

	def __init__(self,x=42.825182,y=-103.000766, zoom=10,showMousePosition=True):
		self.m = folium.Map(location=[x,y], zoom_start=zoom)
		if(showMousePosition):
			enableShowMousePosition(self.m)

	def generateMapFromDao(self,dao,color="green",includeLegend=True):
		style["fillColor"]=color
		# folium.ClickForLatLng().add_to(self.m)
		if(includeLegend):
			self.addMergedLegend(dao)
		for agency in dao.getAgencies():
			layer = self.generateLayerForAgency(agency,color,dao)
			# option for if legends get hooked into layer control. for later.
			# if(includeLegend):
			# 	legendText = "Agency: {} \n\n".format(agency.getValue())
			# 	legendText += "\n".join(getTravelInfoForTripsOfAgencyStrings(dao,agency))
			# 	addLegend(legendText,layer)
		folium.LayerControl().add_to(self.m)
			
	def addMergedLegend(self,dao):
		legendText = ""
		for agency in dao.getAgencies():
			legendText += "Agency: {} \n\n".format(agency.getValue())
			legendText += "\n".join(getTravelInfoForTripsOfAgencyStrings(dao,agency))
		addLegend(legendText,self.m)

	def generateLayerForAgency(self,agency,color,dao):
		folium_layer = folium.FeatureGroup(name = agency.getValue()).add_to(self.m)
		for trip in dao.getTripsForAgency(agency):
			itt = 0
			trip = dao.getGtfsObject(Trip,trip)
			stopsForStopTimes = list()
			for stop_time in trip.stop_times:
				stopsForStopTimes.append(DaoVisualizer.getStopCenterListAndAddStopsToMap(trip.stop_times[stop_time],folium_layer))
			printDebug(['stops for stoptimes: ',stopsForStopTimes])
			self.addLinesToMap(stopsForStopTimes,folium_layer)
		return folium_layer


	def save(self,output_folder):
		self.m.save(output_folder)


	def getStopCenterListAndAddStopsToMap(stop_time,folium_map):
		stops = list()
		st = stop_time
		stop = st.stop
		printDebug(['adding stoptime <',st.getId().getId(),'>  and stop <', str(st.stop.getId().getId()),'> of type: ', str(st.stop.type)])
		if(stop.type==0):
			DaoVisualizer.addStopToMap(stop,folium_map)
		elif(stop.type==1):
			printDebug(['stop ',stop.getId().getId(),' is a location group with ', len(stop.substops), ' substops'])
			for substop in st.stop.substops:
				stop = st.stop.substops[substop]
				DaoVisualizer.addLocationToMap(stop,folium_map)
		else:
			DaoVisualizer.addLocationToMap(stop,folium_map)
		return stop_time.stop.getCenter()
		
	def addLinesToMap(self,locationsForStopTimes,folium_map):
		polyLineCords= list()
		baseCords = list()
		for stop_time_locations in locationsForStopTimes:
			cordsForThisStopTime = list()
			for cord in stop_time_locations:
				# print("cord in stop_time_locations")
				if(cord not in cordsForThisStopTime):
					# print("cord not in cordsForThisStopTime")
					for baseCord in baseCords:
						connectAToBOnMap([baseCord,cord],folium_map)
					if(not cord in baseCords):
						# print("not cord in baseCords")
						cordsForThisStopTime.append(cord)
			# print(cordsForThisStopTime)
			baseCords.extend(cordsForThisStopTime)
			# print(baseCords)

	def addLocationToMap(location,folium_map):
		printDebug(['adding location(stop) to map: ',location.getId().getId()])
		addMarkerWithPopup(
			location.getCenter()[0],
			'location: {}'.format(
				location.getId().getId()),
			folium_map)
		addGeoJsonToMapWithChild(location.initial_data["geometry"],folium.LatLngPopup(),folium_map,style = style)

	def getMap(self):
		return self.m


style = {'fillColor': '#00FFFFFF', 'lineColor': '#00FFFFFF'}
overflowStyle = {"overflow":"scroll"}