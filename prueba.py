#!/usr/bin/python
import datetime
from datetime import timedelta
from operator import itemgetter

###TEST DATA
'''
data = [{"dateTime": "2020-01-30T01:43:30.000","level": "rem","seconds": 180},{"dateTime":"2020-01-30T01:46:30.000","level":"light","seconds":60},{"dateTime":"2020-01-30T01:47:30.000","level":"light","seconds":60}]
shortData=[{"dateTime": "2020-01-30T01:44:30.000","level":"wake","seconds": 60},{"dateTime": "2020-01-30T01:43:40.000","level":"wake","seconds": 10},{"dateTime": "2020-01-30T01:47:20.000","level":"wake","seconds": 20},{"dateTime": "2020-01-30T01:48:00.000","level":"wake","seconds": 20}]
'''
'''
data = [{"dateTime": "2020-01-30T01:43:30.000","level": "rem","seconds": 180},{"dateTime":"2020-01-30T01:46:30.000","level":"light","seconds":60},]
shortData=[{"dateTime": "2020-01-30T01:44:30.000","level":"wake","seconds": 60}]
'''
###END TEST DATA

##Add dataType to every element of both arrays

for stage in data:
	stage['dataType'] = 'data'


for stage in shortData:
	stage['dataType'] = 'shortData'

##Merge both arrays

totalData = data + shortData


for stage in totalData:
	strToDate = datetime.datetime.strptime(stage['dateTime'], '%Y-%m-%dT%H:%M:%S.%f')
	stage['dateTime'] = strToDate




##Arrange totalData rising by dateTime

totalData.sort(key=itemgetter('dateTime'), reverse=True)


##Restructure data algorithm
'''
Compare the current stage with the following.
If they come from the same data there are OK. Just append the current to the new list and the next one return to the gived list in the same place it was.
If they are not the same recalculate the new duration time and append the current and after the next one to the new list. After append both,
Also recalculate the new dateTime for the current stage.
I do it in a while loop because it can have more than 1 short awake while stil in rem/light stage.
When I dont have more stages to look at finish the process.
'''
def restructureData(arrStage):
	finalData = []
	while True:

		try:
			currentStage = arrStage.pop()
		except (IndexError):
			break

		TimeRemeaning = currentStage['seconds']

		while TimeRemeaning >= 0:

			try:
				nextStage = arrStage.pop()
			except (IndexError):
				currentStage['seconds'] = TimeRemeaning
				finalData.append(currentStage)
				break
			
			if currentStage['dataType'] != nextStage['dataType']:
				
				duration = nextStage['dateTime'] - currentStage['dateTime']
				currentStage['seconds'] = duration.total_seconds()

				auxStage = 	{'dateTime': currentStage['dateTime'], 'level': currentStage['level'],'seconds' : currentStage['seconds'],'dataType':  currentStage['dataType']}
				finalData.append(auxStage)
				finalData.append(nextStage)
				
				TimeRemeaning -= currentStage['seconds']
				TimeRemeaning -= nextStage['seconds']

				

				currentStage['dateTime'] += timedelta(seconds = currentStage['seconds'])
				currentStage['dateTime'] += timedelta(seconds = nextStage['seconds'])

			elif TimeRemeaning == 0:
				arrStage.append(nextStage)
				break

			else:
				arrStage.append(nextStage)
				currentStage['seconds'] = TimeRemeaning
				finalData.append(currentStage)
				break


		if TimeRemeaning < 0:
			nextStage = arrStage.pop()
			nextStage['dateTime'] -= timedelta(seconds = TimeRemeaning)
			nextStage['seconds'] += TimeRemeaning
			
			
			arrStage.append(nextStage)


	return finalData



###Clean data to return it in the structure they ask for
finalData = restructureData(totalData)
for data in finalData:
	data['dateTime'] = data['dateTime'].strftime('%Y-%m-%dT%H:%M:%S.%f')
	data['seconds'] = int(data['seconds'])
	del data['dataType']
	print(data)