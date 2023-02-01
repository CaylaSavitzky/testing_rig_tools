"""
author caylasavitzky

turns the travel details of an agency into a string
"""

# import pandas
# import sys
# import json
from flex_models import *
from flex_reader import *








def stringifyBookingInfo(rule):
	out = ""
	if(hasattr(rule,"booking_type")):
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
	# out +="in stop_time " + str(st.getId())
	if(len(st.stop.substops)>0):
		out += "<parent location:" + str(st.stop.getId().getId()) + "> and "
		for substopId in st.stop.substops:
			out += "<location:" + str(substopId) + "> "
	else:
		out += "<location:" + str(st.stop.getId().getId()) + ">"
	if(hasattr(st,"start_pickup_drop_off_window")):
		out += "\n which is allowed between the hours of: " + str(st.start_pickup_drop_off_window) + " and "
	else:
		out += " which has no pickup window and has a dropoff window of "
	if(hasattr(st,"end_pickup_drop_off_window")):
		out += str(st.end_pickup_drop_off_window) +".\n"
	else:
		out += " no end_pickup_drop_off_window"
	if(hasattr(st,"pickup_booking_rule_id")):
		out += stringifyBookingInfo(st.pickup_booking_rule_id)
	elif(hasattr(st,"drop_off_booking_rule_id")):
		out += stringifyBookingInfo(st.drop_off_booking_rule_id)
	else:
		out+= " cannot give more information as stoptime does not have a pickup or drop_off _booking_rule"
	return out


def getTravelInfoForTripsOfAgencyStrings(dao,agency):
	outputStringsContainer = list()
	debug.print(dao.data[Trip])
	debug.print(list(dao.data[Trip].keys())[0])
	debug.print(agency)
	debug.print(agency.getReadable())
	for trip in dao.getTripsForAgency(agency):
		itt = 0
		trip = dao.getGtfsObject(Trip,trip)
		out = "for trip-{}: {}\n".format(
			trip.getId().getId(),trip.getServiceSchedule().strWithoutId())
		stoptimes = trip.stop_times
		stoptimes = sorted(stoptimes.items(),key=lambda x:x[1].stop_sequence)
		for stop_time in stoptimes:
			if(itt==0):
			# if(itt<len(trip.stop_times)-1):
				# if(itt>0):
				# 	out += " and \n"
				out += " travel from: "
			# if(itt==len(trip.stop_times)-1):
			else:
				out += ' to: ' 
			out += stringifyStopTimeOutput(stop_time[1])
			out +="\n"
			itt+=1
		outputStringsContainer.append(out)
	return outputStringsContainer