from dao_printer import *
from zipfile import ZipFile
from daovisualizer import *
import shutil
import os
import sys


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

def processFilesIntoDao(args,dao):
	while len(args)>0:
		# print(sys.argv)
		path = args.pop(0)
		if(not os.path.exists(path)):
			print('could not find: {}'.format(path))
			continue
		if(os.path.isdir(path)):
			print("recursing into directory {}".format(path))
			path = (path if path[-1]=="/" else path+"/")
			debug.print(os.listdir(path))
			args.extend(path+filename for filename in os.listdir(path))
			continue
		if(path[-4:]!=".zip"):
			print("skipping {}".format(path))
			continue
			# should be recursing here mayby?
		data_path = path.split('.')[0]
		unzip(path,data_path)
		FlexReader.readFlexDirectoryIntoDao(data_path,dao)
		# try:
		# 	FlexReader.readFlexDirectoryIntoDao(data_path,dao)
		# except Exception as e:
		# 	print("error occured reading {}: {}".format(data_path,e))
		shutil.rmtree(data_path)

def updateOutputPath(outputPath):
	if(outputPath[-1] =="/"):
		outputPath+="processed_flex_map"
	if(outputPath[-5:]!=".html"):
		outputPath+=".html"
	return outputPath


def run(args,save_graph=True):
	argsString = args.pop(0)

	includeLegend = True
	debug.should_print=False

	arguments = list(filter(lambda arg: arg[0]=="-", sys.argv))

	if("-debug" in arguments or "-d" in arguments):
		print("printing in debug mode")
		debug.should_print=True

	if("-hideLegend" in arguments or "-h" in arguments):
		print("hiding legend")
		includeLegend=False

	args = list(filter(lambda arg: arg[0]!="-", sys.argv))
	debug.print(args)

	outputPath = args.pop()

	dao = DaoImpl()
	processFilesIntoDao(args,dao)

	daoVisualizer = DaoVisualizer()
	daoVisualizer.generateMapFromDao(dao,colors = colorlist,includeLegend=includeLegend)
	outputPath = updateOutputPath(outputPath)
	if(save_graph):
		daoVisualizer.save(outputPath)

	print("firefox "+outputPath)

if __name__ == "__main__":
	run(sys.argv)