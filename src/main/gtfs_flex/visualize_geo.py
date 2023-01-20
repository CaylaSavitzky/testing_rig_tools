import geopandas
import folium
from flex_reader import *
from folium.plugins import MousePosition
import branca.colormap as cm

debug = True
def printDebug(stringstuff):
	if debug == True:
		print(stringstuff)


def addLinesToMap(locationsForStopTimes,folium_map):
	polyLineCords= list()
	baseCords = list()
	for stop_time_locations in locationsForStopTimes:
		cordsForThisStopTime = list()
		for cord in stop_time_locations:
			# print("cord in stop_time_locations")
			if(cord not in cordsForThisStopTime):
				# print("cord not in cordsForThisStopTime")
				for baseCord in baseCords:
					# print("baseCord in baseCords")
					folium.PolyLine([baseCord,cord],style_function=lambda x:style,weight=2.5, opacity=1).add_to(folium_map)
					printDebug(['baseCord&cord: ',[baseCord,cord]])

				if(not cord in baseCords):
					# print("not cord in baseCords")
					cordsForThisStopTime.append(cord)
		# print(cordsForThisStopTime)
		baseCords.extend(cordsForThisStopTime)
		# print(baseCords)


def addMarker(location,folium_map):
	folium.map.Marker(
    [34.0302, -118.2352],
    icon=DivIcon(
        icon_size=(150,36),
        icon_anchor=(0,0),
        html='<div style="font-size: 24pt">Test</div>',
        )
    ).add_to(folium_map)


def addStopToMap(stop,folium_map):
	raise Exception("addStopToMap is not yet implemented")



def addLocationToMap(location,folium_map):
	printDebug(['adding location(stop) to map: ',location.myId])
	folium.GeoJson(location.initial_data["geometry"],style_function=lambda x:style).add_child(folium.Popup('location: '+ str(location.myId))).add_to(folium_map)

def getStopCenterListAndAddStopsToMap(stop_time,folium_map):
	stops = list()
	st = stop_time
	stop = st.stop
	printDebug(['adding stoptime <',st.myId,'>  and stop <', str(st.stop.myId),'> of type: ', str(st.stop.type)])
	if(stop.type==0):
		addStopToMap(stop,map)
	elif(stop.type==1):
		printDebug(['stop ',stop.myId,' is a location group with ', len(stop.substops), ' substops'])
		for substop in st.stop.substops:
			stop = st.stop.substops[substop]
			addLocationToMap(stop,folium_map)
	else:
		addLocationToMap(stop,folium_map)
	return stop_time.stop.getCenter()


def showMousePosition(folium_map):
	formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
	MousePosition(
		position="bottomright",
		separator=" | ",
		empty_string="NaN",
		num_digits=20,
		prefix="Coordinates:",
		lat_formatter=formatter,
		lng_formatter=formatter,
	).add_to(folium_map)
	folium_map.add_child(folium.LatLngPopup())


def addText(folium_map):
	colormap = cm.linear.Set1.scale(0, 35).to_step(10)
	colormap.caption = 'A colormap caption'
	folium_map.add_child(colormap)



def generateMapFromDao(dao,color="green"):
	global m
	style["fillColor"]=color
	# folium_map = folium.FeatureGroup(name = dao.getAgencyName())
	for trip in dao.trips:
		itt = 0
		trip = dao.trips[trip]
		stopsForStopTimes = list()
		for stop_time in trip.stop_times:
			stopsForStopTimes.append(getStopCenterListAndAddStopsToMap(trip.stop_times[stop_time],m))
		printDebug(['stops for stoptimes: ',stopsForStopTimes])
		addLinesToMap(stopsForStopTimes,m)

def start(x=42.825182,y=-103.000766):
	global m
	m = folium.Map(location=[x,y], zoom_start=10)
	showMousePosition(m)

def save(output_folder):
	global m 
	m.save(output_folder)

style = {'fillColor': '#00FFFFFF', 'lineColor': '#00FFFFFF'}
m = None