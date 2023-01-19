import datetime
from datetime import datetime
from datetime import timedelta
from datetime import timezone


class DataInTimeRange:

	def filterDataForTimeRange(minFlagAge,maxFlagAge,data, key):
		now = datetime.now(timezone.utc)
		# print("it is currently " + now.isoformat())

		minFlagAge = timedelta(seconds=minFlagAge)
		minAge = now - minFlagAge
		# print("minimum age of info is: ", minAge.isoformat())

		maxFlagAge = timedelta(seconds=maxFlagAge)
		maxAge = now - maxFlagAge
		# print("minimum age of info is: ", maxAge.isoformat())

		output = list()
		for record in data:
			date = datetime.fromisoformat(record[key])
			# print(date.isoformat())
			if(maxAge<date<minAge):
				output.append(record)
		return output

	def	testFunct():
		print("testFunct")		