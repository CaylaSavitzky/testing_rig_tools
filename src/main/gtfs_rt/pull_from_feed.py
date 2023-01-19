from google.transit import gtfs_realtime_pb2
import urllib.request


class GtfsRtAccessTool:

  def accessGtfs(url, header = None, key = None):
    print(url)
    if url.startswith('file://'):
      localAddress=url.replace('file://', '')
      if(localAddress[-5:].find(".")==-1):
        return open(localAddress, 'rb')
      else:
        return open(localAddress, 'r').read()
    if (key!=None):
      if (header!=None):
        return urllib.request.urlopen(url, header,key)
      else:
        return urllib.request.urlopen(url,key)
    else:
      return urllib.request.urlopen(url)

  def getGtfsEntities(url, header = None, key = None):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = GtfsRtAccessTool.accessGtfs(url, header, key)
    feed.ParseFromString(response.read())
    return feed.entity

  def printGtfsEntities(url, header = None, key = None):
    for entity in GtfsRtAccessTool.getGtfsEntities(url,header,key):
      print(entity)