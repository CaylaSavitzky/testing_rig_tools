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

	def generateMapFromDao(self,dao,colors=['blue','red'],includeLegend=True):
		if(includeLegend):
			self.addMergedLegend(dao)
		agencyItt = 0
		for agency in dao.getAgencies():
			color = colors[agencyItt%len(colors)]
			print("using color {}, for agency {}".format(color,agency.getAgency()))
			style = {'fillColor': color, 'lineColor': color}
			layer = self.generateLayerForAgency(agency,style,dao)
			agencyItt+=1
		folium.LayerControl().add_to(self.m)


			
	def addMergedLegend(self,dao):
		legendText = ""
		for agency in dao.getAgencies():
			print("prepping legend for agency: {}".format(dao.getGtfsObject(Agency,agency).readable))
			legendText += '<span style="font-size:24px">Agency: {}</span> \n\n'.format(dao.getGtfsObject(Agency,agency).readable)
			legendText+="\n".join(getTravelInfoForTripsOfAgencyStrings(dao,agency)).replace("<","&lt;").replace(">","&gt;")
			legendText+="\n\n\n\n"
		addLegend(legendText,self.m)

	def generateLayerForAgency(self,agency,style,dao):
		folium_layer = folium.FeatureGroup(name = dao.getGtfsObject(Agency,agency).readable).add_to(self.m)
		for trip in dao.getTripsForAgency(agency):
			itt = 0
			trip = dao.getGtfsObject(Trip,trip)
			stopsForStopTimes = list()
			for stop_time in trip.stop_times:
				stopsForStopTimes.append(
					DaoVisualizer.getStopCenterListAndAddStopsToMap(
						trip.stop_times[stop_time],
						style,
						dao.getGtfsObject(Agency,agency).readable,
						folium_layer))
			printDebug(['stops for stoptimes: ',stopsForStopTimes])
			self.addLinesToMap(stopsForStopTimes,folium_layer)
		return folium_layer


	def save(self,output_folder):
		self.m.save(output_folder)


	def getStopCenterListAndAddStopsToMap(stop_time, style,readableAgencyName, folium_map):
		stops = list()
		st = stop_time
		stop = st.stop
		printDebug(['adding stoptime <',st.getId().getId(),'>  and stop <', str(st.stop.getId().getId()),'> of type: ', str(st.stop.getType())])
		if(stop.getType()==0):
			DaoVisualizer.addStopToMap(stop,style,readableAgencyName,folium_map)
		elif(stop.getType()==1):
			printDebug(['stop ',stop.getId().getId(),' is a location group with ', len(stop.substops), ' substops'])
			for substop in st.stop.substops:
				stop = st.stop.substops[substop]
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

	def addLocationToMap(location,style,readableAgencyName,folium_map):
		printDebug(['adding location(stop) to map: ',location.getId().getId()])
		addMarkerWithPopup(
			location.getCenter()[0],
			'location: {}{}'.format(readableAgencyName,
				location.getId().getValue()),
			folium_map)
		addGeoJsonToMapWithChild(location.initial_data["geometry"],folium_map,style)

	def addStopToMap(stop,style,readableAgencyName,folium_map):
		printDebug(['adding stop to map: ',stop.getId().getId()])
		addMarkerWithPopup(
			stop.getCenter()[0],
			'stop: {}{}'.format(readableAgencyName,
				stop.getId().getValue()),
			folium_map)
		addCircleToMap(stop.getCenter()[0],style,folium_map)


	def getMap(self):
		return self.m



overflowStyle = {"overflow":"scroll"}