#!/usr/bin/python
import datetime
from datetime import timedelta
'''
data = [{"dateTime": "2020-01-30T01:43:30.000","level": "rem","seconds": 180},{"dateTime":"2020-01-30T01:46:30.000","level":"light","seconds":60},]
shortData=[{"dateTime": "2020-01-30T01:44:30.000","level":"wake","seconds": 60}]
'''
data = [{"dateTime": "2020-01-30T01:43:30.000","level": "rem","seconds": 180},{"dateTime":"2020-01-30T01:46:30.000","level":"light","seconds":60},]
shortData=[{"dateTime": "2020-01-30T01:46:50.000","level":"wake","seconds": 20}]

for dato in data:
	print(dato)

for dato in shortData:
	print(dato)
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

def bubbleSort(arr): 
    n = len(arr)
  
    for i in range(n-1): 
        for j in range(0, n-i-1): 
            if arr[j]['dateTime'] > arr[j+1]['dateTime'] : 
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

totalData = bubbleSort(totalData)

for data in totalData:
	print(data)
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
	i=0
	arrFinal = []
	while i<len(arrStage)-1:
		n=0
		while arrStage[i]['dataType'] != arrStage[i+1+n]['dataType']:
			duration = arrStage[i+1]['dateTime'] - arrStage[i]['dateTime']
			timeRemaining = arrStage[i]['seconds'] - (arrStage[i+1+n]['seconds'] + duration)

			stage = {	
						'dateTime': arrStage[i]['dateTime'],
						'level': arrStage[i]['level'],
						'seconds' : int(duration.total_seconds()),
						'dataType':  arrStage[i]['dataType']
					}

			arrFinal.append(stage) 
			arrFinal.append(arrStage[i+1]) #add next stage to the array also since they will never be 2 shortData in a row.
			seconds = arrStage[i+1]['seconds']
			newDateTime = arrStage[i+1]['dateTime'] + timedelta(seconds=seconds)
			arrStage[i]['dateTime'] = newDateTime
			n += 1

			if i+n+1 >= len(arrStage):
				break
			'''
			we increment this variable to compare the same stage with the after following, maybe it is one more shortData stage before the next data stage
			'''

		if i+n+1 >= len(arrStage):
			arrStage[i]['seconds'] = timeRemaining
			arrFinal.append(arrStage[i])
			break

		if arrStage[i]['dataType'] == arrStage[i+1+n]['dataType']:
			duration = arrStage[i+1+n]['dateTime'] - arrStage[i]['dateTime']
			arrStage[i]['seconds'] = int(duration.total_seconds())
			arrFinal.append(arrStage[i])
		

		i += n+1 #Already checked the i+n position so we dont need to recheck it comparing with the following statges
		

	arrFinal.append(arrStage[i])
	return arrFinal

totalData = restructureData(totalData)
for data in totalData:
	data['dateTime'] = data['dateTime'].strftime('%Y-%m-%dT%H:%M:%S.%f')
	del data['dataType']
	print(data)