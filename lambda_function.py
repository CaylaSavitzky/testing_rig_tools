from dao_printer import *
from zipfile import ZipFile
from daovisualizer import *
from aws_utils import *
import shutil
import os
import boto3
from datetime import datetime


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


gtfs_dir = os.getenv('GTFS_DIRECTORY', '/tmp/gtfs')
output_file = os.getenv('OUTPUT_FILE', '/tmp/gtfs/output.html')
hide_legend = os.getenv('HIDE_LEGEND', False)
debug_output = os.getenv('DEBUG_OUTPUT', False)
s3_bucket = os.getenv('S3_OUTPUT_BUCKET', '')
s3_output_file_path = os.getenv('S3_OUTPUT_PATH', 'index.html')
s3_archive_file_path = os.getenv('S3_ARCHIVE_PATH', 'archive/index-' + datetime.today().strftime('%Y-%m-%d') + ".html")
s3_gtfs_bucket = os.getenv('S3_GTFS_BUCKET', '')
s3_gtfs_file_path = os.getenv('S3_GTFS_FILE_PATH', 'v2qa/input')

s3_client = boto3.client('s3')

def unzip(file,data_path):  
	# loading the temp.zip and creating a zip object
	print("unzipping: {}".format(file))
	with ZipFile(file, 'r') as zObject:
		zObject.extractall(path=data_path)

def processFilesIntoDao(dao):
	download_gtfs()
	for item in os.listdir(gtfs_dir): # loop through items in dir
		if item.endswith(".zip"): # check for ".zip" extension
			gtfs_dir_prefix = gtfs_dir + "/"
			file_name = gtfs_dir_prefix + item # get full path of files
			print("file name is: " + file_name)
			zip_ref = ZipFile(file_name) # create zipfile object
			data_path = gtfs_dir_prefix + item.split(".")[0]
			zip_ref.extractall(data_path) # extract file to dir
			zip_ref.close() # close file
			os.remove(file_name) # delete zipped file
			try:
				FlexReader.readFlexDirectoryIntoDao(data_path,dao)
			except:
				print("error occured reading {}".format(data_path))
			shutil.rmtree(data_path)

def download_gtfs():
	file_names, folders = get_file_folders(s3_client, s3_gtfs_bucket, s3_gtfs_file_path)
	print(file_names)
	print(folders)
	download_files(
		s3_client,
		s3_gtfs_bucket,
		gtfs_dir,
		file_names,
		folders
	)
def lambda_handler(event='', context=''):
	includeLegend = True
	debug.should_print = False

	if(debug_output):
		print("printing in debug mode")
		debug.should_print=True

	if(hide_legend):
		print("hiding legend")
		includeLegend=False


	dao = DaoImpl()
	processFilesIntoDao(dao)

	daoVisualizer = DaoVisualizer()
	daoVisualizer.generateMapFromDao(dao, colors=colorlist, includeLegend=includeLegend)
	daoVisualizer.save(output_file)

	try:
		s3_client.upload_file(output_file, s3_bucket, s3_output_file_path, ExtraArgs={'ContentType': "text/html"})
		s3_client.upload_file(output_file, s3_bucket, s3_archive_file_path, ExtraArgs={'ContentType': "text/html"})
	except Exception as e:
		print(e)


if __name__ == "__main__":
	lambda_handler()