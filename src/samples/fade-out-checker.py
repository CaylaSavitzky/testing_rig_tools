import sys
# import urllib library
from urllib.request import urlopen
# import json
import json
from .. import DataInTimeRange

# store the URL in url as
# parameter for urlopen


env = str(sys.argv[1])
minFlagAge = int(sys.argv[2])
maxFlagAge = int(sys.argv[3])

url = 
comparisonUrl = 

# url = sys.argv[3]
# comparisonUrl = sys.argv[4]

# print("data must be from within : ", str(minFlagAge), " and ", str(maxFlagAge))


# store the response of URL
response = urlopen(url)

# storing the JSON response
# from url in data
data_json = json.loads(response.read())

for record in DataInTimeRange.filterDataForTimeRange(minFlagAge,maxFlagAge,data_json['records'],"time-reported"):
	# print(record)
	target_url = comparisonUrl+record.get("agency-id").replace(" ","%20")+"_"+str(record.get("vehicle-id"));
	# print(target_url)
	comparisonResponse = urlopen(target_url)
	comparison_data_json = json.loads(comparisonResponse.read())
	# print(comparison_data_json.get("Siri").get("ServiceDelivery").get("VehicleMonitoringDelivery"))
	# print(comparison_data_json.get("Siri").get("ServiceDelivery").get("VehicleMonitoringDelivery")[0])
	# print(comparison_data_json.get("Siri").get("ServiceDelivery").get("VehicleMonitoringDelivery")[0].get("VehicleActivity"))
	if(comparison_data_json.get("Siri").get("ServiceDelivery").get("VehicleMonitoringDelivery")[0].get("VehicleActivity")!= None):
		print(comparison_data_json.get("Siri").get("ServiceDelivery").get("VehicleMonitoringDelivery")[0].get("VehicleActivity")[0].get("MonitoredVehicleJourney").get("LineRef"),
			comparison_data_json.get("Siri").get("ServiceDelivery").get("VehicleMonitoringDelivery")[0].get("VehicleActivity")[0].get("MonitoredVehicleJourney").get("VehicleRef"),
			sep=',')
	



# compare it to: https://bustime.mta.info/api/siri/vehicle-monitoring.json?key=OBANYC&callback=jsonp1673295003251&_=1673295003731&OperatorRef=MTA%20NYCT&VehicleRef=MTA%20NYCT_374
# agency-id + '_' + vehicle-id