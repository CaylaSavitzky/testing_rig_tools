import geopandas
import folium
from flex_reader import *
from folium.plugins import MousePosition, FloatImage
import branca
from FloatDiv import FloatDiv



from PIL import Image, ImageDraw, ImageFont
import base64


JENKITY_PAGE_WIDTH = 920


"""
an incredibly messy method where we convert text into an image and then
cover half the page with that image because there are no other pre-existing 
abosolute possitioned items in folium
"""
def addLegend(text,folium_map):
	print("using map {}".format(folium_map))
	text=text.replace("<","&lt;").replace(">","&gt;")
	out = '<p style="padding: 24px; white-space: pre-wrap; font-size : 24; background-color : black; color : white;">{}</p>'.format(text)
	FloatDiv(out,left=0,bottom=0).add_to(folium_map)





debug = False
def printDebug(stuffToPrint):
	if debug == True:
		print("".join(str(item) for item in stuffToPrint))


def connectAToBOnMap(cordPair,folium_map):
	# please make this an arrow
	# folium.PolyLine(cordPair,style_function=lambda x:style,weight=2.5, opacity=1).add_to(folium_map)
	printDebug(['pretend these were added: baseCord&cord: ',cordPair])




def addMarkerWithPopup(latLon,message,folium_map):
	# print(latLon)
	folium.map.Marker(
    [latLon[0], latLon[1]],
    popup=folium.Popup(message,show=True,sticky=True)
    ).add_to(folium_map)
	# text = 'your text here'

	# iframe = folium.IFrame(text, width=700, height=450)
	# popup = folium.Popup(iframe, max_width=3000)

	# Text = folium.Marker(location=[latLon[0], latLon[1]], popup=popup,
	#                      icon=folium.Icon(icon_color='green'))
	# m.add_child(text)


def addStopToMap(stop,folium_map):
	folium.Circle(stop.getCenter()[0]).add_to(folium_map)


def addGeoJsonToMapWithChild(geoJson,child,folium_map,style = None, noLatLongPopup=False):
	folium.GeoJson(geoJson,style_function=lambda x:style).add_to(folium_map)

def createStickyPopup(text):
	return folium.Popup(text,show=True,sticky=True)


def enableShowMousePosition(folium_map):
	# formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
	# MousePosition(
	# 	position="bottomright",
	# 	separator=" | ",
	# 	empty_string="NaN",
	# 	num_digits=20,
	# 	prefix="Coordinates:",
	# 	lat_formatter=formatter,
	# 	lng_formatter=formatter,
	# ).add_to(folium_map)
	folium_map.add_child(folium.LatLngPopup())


# def addLegend(text,folium_map=None):
# 	if(folium_map == None):
# 		global m
# 		folium_map = m
# 	colormap = branca.colormap.linear.YlOrRd_09.scale(0, 8500)
# 	print (text)
# 	colormap.caption = text
# 	folium_map.add_child(colormap)
	



