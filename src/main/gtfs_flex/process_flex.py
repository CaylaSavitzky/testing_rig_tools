from flex_cli import *
from zipfile import ZipFile
from daovisualizer import *
import shutil


#colorlist=["#7e9a9a","#f6d8ac","#db9833","#2a6592","#8ec3eb"]

colorlist=[
"#ffb5bA",
"#be0032",
"#f38400",
"#f3c300",
"#008856",
"#00a1c2",
"#9a4eae",
"#9a4eae"]



def unzip(file,data_path):  
	# loading the temp.zip and creating a zip object
	with ZipFile(file, 'r') as zObject:
		zObject.extractall(path=data_path)

argvItt = 1
includeLegend = True
if(sys.argv[argvItt]=="hideLegend"):
	includeLegend=False
	argvItt+=1

dao = DaoImpl()
daoVisualizer = DaoVisualizer()
while argvItt<len(sys.argv)-1:
	file = sys.argv[argvItt]
	data_path = sys.argv[argvItt].split('.')[0]
	unzip(file,data_path)
	FlexReader.readFlexDirectoryIntoDao(data_path,dao)
	shutil.rmtree(data_path)
	argvItt+=1

daoVisualizer.generateMapFromDao(dao,colors = colorlist,includeLegend=includeLegend)
if(sys.argv[argvItt][-1] =="/"):
	sys.argv[argvItt]+="processed_flex_map"
daoVisualizer.save(sys.argv[argvItt]+".html")


print("firefox "+data_path+"-map.html")


