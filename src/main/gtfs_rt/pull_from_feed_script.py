#!/usr/bin/env python

# python3.11 pull_from_feed_script.py http://gtfsrt.prod.wmata.obaweb.org:8080/api/v1/key/4b248c1b/agency/1/command/gtfs-rt/tripUpdates

from google.transit import gtfs_realtime_pb2
import urllib.request
import sys
from pull_from_feed import GtfsRtAccessTool

gtfsRtAccessTool = GtfsRtAccessTool()
feed = gtfs_realtime_pb2.FeedMessage()
response = None
if(len(sys.argv)==2):
	GtfsRtAccessTool.printGtfsEntities(sys.argv[1])
if(len(sys.argv)==3):
	GtfsRtAccessTool.printGtfsEntities(sys.argv[1],sys.argv[2])
if(len(sys.argv)==4):
	GtfsRtAccessTool.printGtfsEntities(sys.argv[1],sys.argv[2],sys.argv[3])
