from dao_printer import *
from zipfile import ZipFile
from daovisualizer import *
import shutil
import os


colorlist=[
"slateblue",
"coral",
"maroon",
"goldenrod",
"midnightblue",
"crimson",
"mediumseagreen",
"olive",
"deepskyblue",
"darkorange"]



def unzip(file,data_path):  
	# loading the temp.zip and creating a zip object
	print("unzipping: {}".format(file))
	with ZipFile(file, 'r') as zObject:
		zObject.extractall(path=data_path)

argsString = sys.argv.pop(0)

includeLegend = True
if(sys.argv[0]=="-hideLegend"or sys.argv[0]== "-h"):
	includeLegend=False
	sys.argv.pop(0)




outputPath = sys.argv.pop()

dao = DaoImpl()
daoVisualizer = DaoVisualizer()
while len(sys.argv)>0:
	# print(sys.argv)
	path = sys.argv.pop(0)
	if(not os.path.exists(path)):
		print('could not find: {}'.format(path))
		continue
	if(os.path.isdir(path)):
		print("recursing into directory {}".format(path))
		printDebug(os.listdir(path))
		path = (path if path[-1]=="/" else path+"/")
		sys.argv.extend(path+filename for filename in os.listdir(path))
		continue
	if(path[-4:]!=".zip"):
		print("skipping {}".format(path))
		continue
		# should be recursing here mayby?
	data_path = path.split('.')[0]
	unzip(path,data_path)
	FlexReader.readFlexDirectoryIntoDao(data_path,dao)
	shutil.rmtree(data_path)


daoVisualizer.generateMapFromDao(dao,colors = colorlist,includeLegend=includeLegend)
if(outputPath[-1] =="/"):
	outputPath+="processed_flex_map"
if(outputPath[-5:]!=".html"):
	outputPath+=".html"
daoVisualizer.save(outputPath)

print("firefox "+outputPath)


