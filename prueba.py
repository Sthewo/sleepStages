#!/usr/bin/python
import datetime
from datetime import timedelta
from operator import itemgetter

###TEST DATA

#Random example
'''
rawData = 	{"level":{
				"data":
						[
							{"dateTime": "2020-01-30T01:43:30.000","level": "rem","seconds": 180},
							{"dateTime":"2020-01-30T01:46:30.000","level":"light","seconds":60},
							{"dateTime":"2020-01-30T01:47:30.000","level":"rem","seconds":60}
						],
				"shortData":
						[
							{"dateTime": "2020-01-30T01:44:30.000","level":"wake","seconds": 60},
							{"dateTime": "2020-01-30T01:43:40.000","level":"wake","seconds": 10},
							{"dateTime": "2020-01-30T01:47:20.000","level":"wake","seconds": 20},
							{"dateTime": "2020-01-30T01:48:00.000","level":"wake","seconds": 20}
						]
				}
			}

'''

#Problem example
'''
rawData = 	{"level":{
				"data":
						[
							{"dateTime": "2020-01-30T01:43:30.000","level": "rem","seconds": 180},
							{"dateTime":"2020-01-30T01:46:30.000","level":"light","seconds":60}
						],
				"shortData":
						[
							{"dateTime": "2020-01-30T01:44:30.000","level":"wake","seconds": 60}
						]
				}
			}

'''
###END TEST DATA



##Restructure data algorithm
'''
Compare the current stage with the following.
If they come from the same data there are OK. Just append the current to the new list and the next one return to the gived list in the same place it was.
If they are not the same recalculate the new duration time and append the current and after the next one to the new list. After append both,
Also recalculate the new dateTime for the current stage.
I do it in a while loop because it can have more than 1 short awake while stil in rem/light stage.
When I dont have more stages to look at finish the process.
The list must be order in descending order by dateTime
'''

def restructureData(arrStage):#The list must be order in descending order by dateTime

		#list to store the restructured data
		finalData = []


		while arrStage:

			#Take the first stage
			currentStage = arrStage.pop()

			#save the time that still having, because the stage could be splited in more stages, so I will use it to recalculete the direfent split stages 
			timeRemaining = currentStage['seconds']

			#If there is time remaining that means could be more shortDate stages before the end of the current stage
			while timeRemaining >= 0:

				#get the next stage to compare and see what kind of stage it is. 
				#If there is no more stages to pop() the exept just set the timeRemaining to the last stage, save it in the finalData list and braek the loop
				try:
					nextStage = arrStage.pop()
				except (IndexError):
					currentStage['seconds'] = timeRemaining
					finalData.append(currentStage)
					break
				
				#if the current stage type is diferent from the next that means current stage is data and the next stage is shortData
				#we proceed to split the current stage and recalculete where it continuos after the nextStage
				if currentStage['dataType'] != nextStage['dataType']:
					
					duration = nextStage['dateTime'] - currentStage['dateTime']
					currentStage['seconds'] = duration.total_seconds()

					#I use and auxiliar stage to save the data in the final list because if not there is some troubles with the pointers saved in the list
					auxStage = 	{'dateTime': currentStage['dateTime'], 'level': currentStage['level'],'seconds' : currentStage['seconds'],'dataType':  currentStage['dataType']}
					finalData.append(auxStage)
					finalData.append(nextStage)
					
					#recalculate the time remaining for the following split stages of the current stage
					timeRemaining -= currentStage['seconds']
					timeRemaining -= nextStage['seconds']

					
					#set where the following split stage should continuous
					currentStage['dateTime'] += timedelta(seconds = currentStage['seconds'])
					currentStage['dateTime'] += timedelta(seconds = nextStage['seconds'])

				#if there is no time remaining just return to arrStage the next stage and break the loop, because the current stage is over
				elif timeRemaining == 0:
					arrStage.append(nextStage)
					break

				#if there is time remaining and the next stage is of the same type, save the current stage with the time remaining and return the next stage to arrStage 
				else:
					arrStage.append(nextStage)
					currentStage['seconds'] = timeRemaining
					finalData.append(currentStage)
					break

			#This case is when a shortDate is lapsed between two data. So instead of recalculate where the current stage should continuous we need to recalculete where the next stage should start
			if timeRemaining < 0:
				#take it to modify dateTime and duration
				nextStage = arrStage.pop()

				#beacause the seconds<0, I do inverse operation that I really need
				#dateTime will be later so I need to add seconds to it (substract) 
				#seconds will be less so I need to substract to it (add)
				nextStage['dateTime'] -= timedelta(seconds = timeRemaining)
				nextStage['seconds'] += timeRemaining
				
				
				arrStage.append(nextStage)


		return finalData

def sleepingStages(rawData):

	##Add dataType to every element of both arrays
	for stage in rawData['level']['data']:
		stage['dataType'] = 'data'

	for stage in rawData['level']['shortData']:
		stage['dataType'] = 'shortData'


	##Merge both arrays
	totalData = rawData['level']['data'] + rawData['level']['shortData']


	##From string to dateTime type
	for stage in totalData:
		strToDate = datetime.datetime.strptime(stage['dateTime'], '%Y-%m-%dT%H:%M:%S.%f')
		stage['dateTime'] = strToDate


	##Arrange totalData decresing by dateTime
	totalData.sort(key=itemgetter('dateTime'), reverse=True)


	##apply the algorithm
	finalData = restructureData(totalData)


	###Clean data to return it in the structure they ask for
	for data in finalData:
		data['dateTime'] = data['dateTime'].strftime('%Y-%m-%dT%H:%M:%S.%f')
		data['seconds'] = int(data['seconds'])
		del data['dataType']
		#uncoment below line to print date on screen
		#print(data)

	return finalData



	

#sleepingStages(rawData)
