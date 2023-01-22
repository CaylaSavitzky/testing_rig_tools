from flex_cli import *
from visualize_geo import *
from zipfile import ZipFile
import shutil


def unzip(file,data_path):  
	# loading the temp.zip and creating a zip object
	with ZipFile(file, 'r') as zObject:
		zObject.extractall(path=data_path)


file = sys.argv[1]
data_path = sys.argv[1].split('.')[0]
unzip(file,data_path)


color = 'red'
dao = readFlexData(data_path)
start()
generateMapFromDao(dao,color = color)
out = ""
for text in getTravelInfoForTripsStrings(dao):
		out+=text+"\n"
addLegend(out,address=data_path+'-image.png')
save(data_path+"-map.html")

shutil.rmtree(data_path)