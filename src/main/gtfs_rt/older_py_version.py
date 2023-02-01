#!/usr/bin/env python

# use sample ./git_api_body.py http://internaldata.mta.info/mnr/gtfs-mnr x-api-key nsmUmqAo5Y6U6ys3LW3O858cvQwAOiRH7XZnNPDQ | less

import random
import sys
import time
import urllib2
from google.transit import gtfs_realtime_pb2


feed = gtfs_realtime_pb2.FeedMessage()

url = sys.argv[1]
if len(sys.argv) > 2:
  print ("using key " + sys.argv[3])
  header = sys.argv[2]
  key = sys.argv[3]
else:
  print ("using embedded key")
  header = 'x-api-key'
  #header = 'api_key_header'
  key = 'nsmUmqAo5Y6U6ys3LW3O858cvQwAOiRH7XZnNPDQ'
req = urllib2.Request(url)
req.add_header(header, key)
req.add_header('Accept', 'application/x-protobuf')
#req.add_header('Accept', 'application/x-google-protobuf')
if url.startswith('file://'):
  gtfs_raw = open(url.replace('file://', ''), 'r').read()
else:
  gtfs_raw = urllib2.urlopen(req).read()

# parse the raw feed
feed.ParseFromString(gtfs_raw)

# access the data structure as needed
#print feed.header.timestamp
#print feed.header.gtfs_realtime_version
#print(str(feed.header.timestamp))
#print(str(feed.header.gtfs_realtime_version))
print(str(feed.header))
for entity in feed.entity:
  print(str(entity))