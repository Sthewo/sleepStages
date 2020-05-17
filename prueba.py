#!/usr/bin/python
import datetime
from datetime import timedelta
from operator import itemgetter

data = [{"dateTime": "2020-01-30T01:43:30.000","level": "rem","seconds": 180},{"dateTime":"2020-01-30T01:46:30.000","level":"light","seconds":60},{"dateTime":"2020-01-30T01:47:30.000","level":"light","seconds":60}]
shortData=[{"dateTime": "2020-01-30T01:44:30.000","level":"wake","seconds": 60},{"dateTime": "2020-01-30T01:43:40.000","level":"wake","seconds": 10}]
'''
data = [{"dateTime": "2020-01-30T01:43:30.000","level": "rem","seconds": 180},{"dateTime":"2020-01-30T01:46:30.000","level":"light","seconds":60},]
shortData=[{"dateTime": "2020-01-30T01:44:30.000","level":"wake","seconds": 60}]
'''

##
##Add dataType to every element of both arrays

for stage in data:
	stage['dataType'] = 'data'


for stage in shortData:
	stage['dataType'] = 'shortData'

##
##Merge both arrays

totalData = data + shortData


for stage in totalData:
	strToDate = datetime.datetime.strptime(stage['dateTime'], '%Y-%m-%dT%H:%M:%S.%f')
	stage['dateTime'] = strToDate



##
##Arrange totalData rising by dateTime

totalData.sort(key=itemgetter('dateTime'), reverse=True)
'''def bubbleSort(arr): 
    n = len(arr)
  
    for i in range(n-1): 
        for j in range(0, n-i-1): 
            if arr[j]['dateTime'] > arr[j+1]['dateTime'] : 
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

totalData = bubbleSort(totalData)'''

#
##Restructure data algorithm
'''
Compare the current stage with the following.
If they come from the same initial there is not any option that they have to reorganize the stages.
If they are not the same recalculate the new duration time.
I do it in a while loop because it can have more than 1 short awake while stil in rem.
If they have the same dataType do nothing.
'''
def restructureData(arrStage):
	finalData = []
	for currentStage in arrStage:
		arrStage.pop()
		TimeRemeaning = currentStage['seconds']

		while TimeRemeaning >= 0:
			nextStage = arrStage.pop()

			if currentStage['dataType'] != nextStage['dataType']:

				duration = nextStage['dateTime'] - currentStage['dateTime']
				currentStage['seconds'] = duration.total_seconds()

				finalData = append(currentStage)
				finalData = append(nextStage)

				TimeRemeaning -= currentStage['seconds']
				TimeRemeaning -= nextStage['seconds']

				currentStage['dateTime'] += discardStage['seconds']
				currentStage['dateTime'] += nextStage['seconds']

			elif TimeRemeaning == 0:
				arrStage.append(nextStage)

			else:
				arrStage.append(nextStage)
				currentStage['seconds'] = TimeRemeaning
				finalData = append(currentStage)

		if currentStage['dataType'] == nextStage['dataType'] and TimeRemeaning < 0:

			nextStage = arrStage.pop()
			dateTime = nextStage['dateTime'] - TimeRemeaning
			nextStage['dateTime'] = dateTime
			arrStage.append(nextStage)

	return finalData


finalData = restructureData(totalData)
for data in finalData:
	data['dateTime'] = data['dateTime'].strftime('%Y-%m-%dT%H:%M:%S.%f')
	del data['dataType']
	print(data)#!/usr/bin/python
import datetime
from datetime import timedelta
from operator import itemgetter

data = [{"dateTime": "2020-01-30T01:43:30.000","level": "rem","seconds": 180},{"dateTime":"2020-01-30T01:46:30.000","level":"light","seconds":60},{"dateTime":"2020-01-30T01:47:30.000","level":"light","seconds":60}]
shortData=[{"dateTime": "2020-01-30T01:44:30.000","level":"wake","seconds": 60},{"dateTime": "2020-01-30T01:43:40.000","level":"wake","seconds": 10}]
'''
data = [{"dateTime": "2020-01-30T01:43:30.000","level": "rem","seconds": 180},{"dateTime":"2020-01-30T01:46:30.000","level":"light","seconds":60},]
shortData=[{"dateTime": "2020-01-30T01:44:30.000","level":"wake","seconds": 60}]
'''

##
##Add dataType to every element of both arrays

for stage in data:
	stage['dataType'] = 'data'


for stage in shortData:
	stage['dataType'] = 'shortData'

##
##Merge both arrays

totalData = data + shortData


for stage in totalData:
	strToDate = datetime.datetime.strptime(stage['dateTime'], '%Y-%m-%dT%H:%M:%S.%f')
	stage['dateTime'] = strToDate



##
##Arrange totalData rising by dateTime

totalData.sort(key=itemgetter('dateTime'), reverse=True)
'''def bubbleSort(arr): 
    n = len(arr)
  
    for i in range(n-1): 
        for j in range(0, n-i-1): 
            if arr[j]['dateTime'] > arr[j+1]['dateTime'] : 
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

totalData = bubbleSort(totalData)'''

#
##Restructure data algorithm
'''
Compare the current stage with the following.
If they come from the same initial there is not any option that they have to reorganize the stages.
If they are not the same recalculate the new duration time.
I do it in a while loop because it can have more than 1 short awake while stil in rem.
If they have the same dataType do nothing.
'''
def restructureData(arrStage):
	finalData = []
	for currentStage in arrStage:
		arrStage.pop()
		TimeRemeaning = currentStage['seconds']

		while TimeRemeaning >= 0:
			nextStage = arrStage.pop()

			if currentStage['dataType'] != nextStage['dataType']:

				duration = nextStage['dateTime'] - currentStage['dateTime']
				currentStage['seconds'] = duration.total_seconds()

				finalData = append(currentStage)
				finalData = append(nextStage)

				TimeRemeaning -= currentStage['seconds']
				TimeRemeaning -= nextStage['seconds']

				currentStage['dateTime'] += discardStage['seconds']
				currentStage['dateTime'] += nextStage['seconds']

			elif TimeRemeaning == 0:
				arrStage.append(nextStage)

			else:
				arrStage.append(nextStage)
				currentStage['seconds'] = TimeRemeaning
				finalData = append(currentStage)

		if currentStage['dataType'] == nextStage['dataType'] and TimeRemeaning < 0:

			nextStage = arrStage.pop()
			dateTime = nextStage['dateTime'] - TimeRemeaning
			nextStage['dateTime'] = dateTime
			arrStage.append(nextStage)

	return finalData


finalData = restructureData(totalData)
for data in finalData:
	data['dateTime'] = data['dateTime'].strftime('%Y-%m-%dT%H:%M:%S.%f')
	del data['dataType']
	print(data)