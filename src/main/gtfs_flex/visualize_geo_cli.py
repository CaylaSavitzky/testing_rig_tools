import geopandas
import sys
import folium
from flex_reader import *
from visualize_geo import *




# folium.map.Marker(
#     [34.0302, -118.2352],
#     icon=DivIcon(
#         icon_size=(150,36),
#         icon_anchor=(0,0),
#         html='<div style="font-size: 24pt">Test</div>',
#         )
#     ).add_to(m)








folder = sys.argv[1]
if(len(sys.argv)>2):
	raise Exception("currently only works with one option")
dao = readFlexData(folder)
generateMapFromDao(dao,folder+"/map.html")