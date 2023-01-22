import geopandas
import folium
from flex_reader import *
from folium.plugins import MousePosition, FloatImage
import branca



from PIL import Image, ImageDraw, ImageFont
import base64


JENKITY_PAGE_WIDTH = 920




def addLegend(text,folium_map=None, address="pycoatextlogo.png"):
	if(folium_map == None):
		global m
		folium_map = m
	# image_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2lSt_kAW9koUo_rHtER8WedSICXdvl8c7_Q&usqp=CAU"
	# iframe = folium.IFrame(text, width=700, height=450)
	# popup = folium.Popup(iframe, max_width=3000)
	# textContainer = folium.Tooltip(text)
	# FloatImage(image_link, bottom=50, left=50, tooltip="testing").add_to(folium_map)
	global JENKITY_PAGE_WIDTH
	W, H = (JENKITY_PAGE_WIDTH,1000)
	im = Image.new("RGBA",(W,H))
	draw = ImageDraw.Draw(im)
	msg = text
	w, h = draw.textsize(msg)
	fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 18)

	# if img.size[0] > img.size[1]:
	# 	shorter = img.size[1]
	# 	llx, lly = (img.size[0]-img.size[1]) // 2 , 0
	# else:
	# 	shorter = img.size[0]
	# 	llx, lly = 0, (img.size[1]-img.size[0]) // 2
	draw.rectangle(((0,0),(W,H)), fill=(0,0,0)+(255,))
	draw.multiline_text((20,0), msg, font=fnt,fill=(255, 255, 255))
	im.save(address, "PNG")
	print(address)
	with open(address, 'rb') as lf:
		# open in binary mode, read bytes, encode, decode obtained bytes as utf-8 string
		b64_content = base64.b64encode(lf.read()).decode('utf-8')
		FloatImage('data:image/png;base64,{}'.format(b64_content), bottom=0, left=0).add_to(folium_map)
		# FloatImage(b64_content, bottom=0, left=0).add_to(m)





debug = True
def printDebug(stuffToPrint):
	if debug == True:
		print("".join(str(item) for item in stuffToPrint))


def connectAToBOnMap(cordPair,folium_map):
	# please make this an arrow
	# folium.PolyLine(cordPair,style_function=lambda x:style,weight=2.5, opacity=1).add_to(folium_map)
	printDebug(['pretend these were added: baseCord&cord: ',cordPair])

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
					connectAToBOnMap([baseCord,cord],folium_map)
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
	text = 'your text here'

	iframe = folium.IFrame(text, width=700, height=450)
	popup = folium.Popup(iframe, max_width=3000)

	Text = folium.Marker(location=[lat,lon], popup=popup,
	                     icon=folium.Icon(icon_color='green'))
	m.add_child(text)


def addStopToMap(stop,folium_map):
	folium.Circle(stop.getCenter()[0]).add_to(folium_map)



def addLocationToMap(location,folium_map):
	printDebug(['adding location(stop) to map: ',location.myId])
	folium.GeoJson(location.initial_data["geometry"],style_function=lambda x:style).add_child(folium.Popup('location: '+ str(location.myId))).add_to(folium_map)

def getStopCenterListAndAddStopsToMap(stop_time,folium_map):
	stops = list()
	st = stop_time
	stop = st.stop
	printDebug(['adding stoptime <',st.myId,'>  and stop <', str(st.stop.myId),'> of type: ', str(st.stop.type)])
	if(stop.type==0):
		addStopToMap(stop,folium_map)
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


# def addLegend(text,folium_map=None):
# 	if(folium_map == None):
# 		global m
# 		folium_map = m
# 	colormap = branca.colormap.linear.YlOrRd_09.scale(0, 8500)
# 	print (text)
# 	colormap.caption = text
# 	folium_map.add_child(colormap)
	


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