from flex_cli import *
from zipfile import ZipFile
from daovisualizer import *
import shutil


def unzip(file,data_path):  
	# loading the temp.zip and creating a zip object
	with ZipFile(file, 'r') as zObject:
		zObject.extractall(path=data_path)


file = sys.argv[1]
data_path = sys.argv[1].split('.')[0]
unzip(file,data_path)


color = 'red'
dao = DaoImpl()
FlexReader.readFlexDirectoryIntoDao(data_path,dao)
daoVisualizer = DaoVisualizer()

includeLegend = True
# out = ""
# for agency in dao.getAgencies():
# 	out = "Agency: {} \n\n".format(agency.getValue())
# 	out += "\n".join(getTravelInfoForTripsOfAgencyStrings(dao,agency))
if(len(sys.argv)>2):
	# probably should add some options here
	# print(out)	
	includeLegend = False
# else:
# 	addLegend(out,daoVisualizer.getMap())
daoVisualizer.generateMapFromDao(dao,color = color,includeLegend=includeLegend)
daoVisualizer.save(data_path+"-map.html")

shutil.rmtree(data_path)


import os
command = " /bin/bash -c firefox "+data_path+"-map.html"
print("firefox "+data_path+"-map.html")
os.system(command)

