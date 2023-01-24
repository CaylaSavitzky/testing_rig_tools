from visualize_geo import *
"""
takes dao and creates map
"""

class DaoVisualizer:

	def __init__(self,x=42.825182,y=-103.000766, zoom=10,showMousePosition=True):
		self.m = folium.Map(location=[x,y], zoom_start=zoom)
		if(showMousePosition):
			enableShowMousePosition(self.m)

	def generateMapFromDao(self,dao,color="green"):
		style["fillColor"]=color
		# folium_map = folium.FeatureGroup(name = dao.getAgencyName())
		for trip in dao.getTrips():
			itt = 0
			trip = dao.getGtfsObject(Trip,trip)
			stopsForStopTimes = list()
			for stop_time in trip.stop_times:
				stopsForStopTimes.append(DaoVisualizer.getStopCenterListAndAddStopsToMap(trip.stop_times[stop_time],self.m))
			printDebug(['stops for stoptimes: ',stopsForStopTimes])
			self.addLinesToMap(stopsForStopTimes,self.m)

	def save(self,output_folder):
		self.m.save(output_folder)


	def getStopCenterListAndAddStopsToMap(stop_time,folium_map):
		stops = list()
		st = stop_time
		stop = st.stop
		printDebug(['adding stoptime <',st.getId(),'>  and stop <', str(st.stop.getId()),'> of type: ', str(st.stop.type)])
		if(stop.type==0):
			DaoVisualizer.addStopToMap(stop,folium_map)
		elif(stop.type==1):
			printDebug(['stop ',stop.getId(),' is a location group with ', len(stop.substops), ' substops'])
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
		printDebug(['adding location(stop) to map: ',location.getId()])
		popup = createStickyPopup('location: {}'.format(location.getId()))
		addGeoJsonToMapWithChild(location.initial_data["geometry"],popup,folium_map,style = style)

	def getMap(self):
		return self.m
style = {'fillColor': '#00FFFFFF', 'lineColor': '#00FFFFFF'}
overflowStyle = {"overflow":"scroll"}