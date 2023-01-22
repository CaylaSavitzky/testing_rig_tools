# /Users/caylasavitzky/Downloads/chadroncitytransit-ne-us--flex-v2/stop_times.txt

import pandas
import sys
import json
from flex_models import *
from flex_reader import *




# class ServiceId:
# 	def __init__(self, initial_data):
# 		for key in initial_data:
# 			setattr(self, key, initial_data[key])







def stringifyBookingInfo(rule):
	out = ""
	if(rule.booking_type==2):
		out += "  Make sure to book at most " + str(rule.prior_notice_start_day) + " days beforehand after " + str(rule.prior_notice_start_time)
		out += " and at least "+str(rule.prior_notice_last_day) +" days beforehand by " + str(rule.prior_notice_last_time)
	else:
		out += "  Make sure to book at least " + str(rule.prior_notice_duration_min) +" minutes beforehand "
	if((rule.booking_type==1) and (rule.prior_notice_duration_max!=None)):
		out += " and at most " + str(rule.prior_notice_duration_max) + " minutes beforehand"
	return out;

def stringifyStopTimeOutput(st):
	out = ""
	# out +="in stop_time " + str(st.myId)
	if(len(st.stop.substops)>0):
		out += "<parent location:" + str(st.stop.myId) + "> and "
		for substop in st.stop.substops:
			out += "<location:" + str(substop) + "> "
	else:
		out += "<location:" + str(st.stop.myId) + ">"
	out += "\n which is allowed between the hours of: " + str(st.start_pickup_drop_off_window)
	out += " and " + str(st.end_pickup_drop_off_window) +".\n"
	if(isNotNullOrNan(st.pickup_booking_rule_id)):
		if(isNotNullOrNan(st.drop_off_booking_rule)):
			out += stringifyBookingInfo(st.pickup_booking_rule)
	else:
		out+= " cannot give more information as stoptime does not have a pickup or drop_off _booking_rule"
	return out


def getTravelInfoForTripsStrings(dao):
	outputStringsContainer = list()
	for trip in dao.trips:
		out = "for trip-{}: \n".format(trip)
		itt = 0
		trip = dao.trips[trip]
		for stop_time in trip.stop_times:
			if(itt==0):
			# if(itt<len(trip.stop_times)-1):
				# if(itt>0):
				# 	out += " and \n"
				out += " travel from: "
			# if(itt==len(trip.stop_times)-1):
			else:
				out += ' to: ' 
			out += stringifyStopTimeOutput(trip.stop_times[stop_time])
			out +="\n"
			itt+=1
		outputStringsContainer.append(out)
	return outputStringsContainer







if __name__ == "__main__":
	print("running flex_cli")
	folder = sys.argv[1]

	dao = readFlexData(folder)

	# for trip in dao.trips:
	# 	out = print("\n",trip, dao.trips[trip])
	# 	for stop_time in dao.trips[trip].stop_times:
	# 		st = dao.trips[trip].stop_times[stop_time]
	# 		print(str(st.myId), str(st.stop.myId))

	for out in getTravelInfoForTripsStrings(dao):
		print(out+"\n")