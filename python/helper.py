import MySQLdb
import hashlib
import uuid
import datetime
from datetime import date
try: import simplejson as json
except ImportError: import json

def connectDb():
    connection = MySQLdb.connect("localhost","cwajazz9_vms","radio#492*","cwajazz9_vms")
    cursor = connection.cursor()
    return cursor, connection

def sendJson(*json_objects):
    data = {}
    for items in json_objects:
        data.update(items)
    return json.JSONEncoder().encode(data)

def encrypt(password):
    salt = uuid.uuid4().hex
    hashed = hashlib.sha512(salt+password).hexdigest()
    return hashed, salt

def hour_period_to_node(time_period):
	out = []
	start = int(time_period[0:2])
	end = int(time_period[6:8])
	if(start == end):
		if (end<10):
			out.append('0'+str(end)+':00')
		else:
			out.append(str(end)+':00')
	else:
		for i in range(start,end):
			if (i<10):
				out.append('0'+str(i)+':00')
				out.append('0'+str(i)+':30')
			else:
				out.append(str(i)+':00')
				out.append(str(i)+':30')

		if (int(time_period[3]) == 3):
			out = out[1:len(out)]
		if (int(time_period[9]) == 3):
			if (end<10):
				out.append('0'+str(end)+':00')
			else:
				out.append(str(end)+':00')
	return out

def year(datetime):
	return int(datetime[0:4])

def month(datetime):
	return int(datetime[5:7])

def day(datetime):
	return int(datetime[8:10])

def hour(datetime):
	return int(datetime[11:13])

def minute(datetime):
	return int(datetime[14:16])

def myDate(datetime):
	return datetime[0:10]

def time(datetime):
	return datetime[11:16]

def days_diff(datetime_start,datetime_end):
	datetime_start = date(year(datetime_start),month(datetime_start),day(datetime_start))
	datetime_end = date(year(datetime_end),month(datetime_end),day(datetime_end))
	days = datetime_end - datetime_start
	return days.days

def hour_period_to_node_with_single_date(datetime_start,datetime_end):
	datetimeNodes = []
	for node in hour_period_to_node(time(datetime_start)+' '+time(datetime_end)):
		datetimeNodes.append(myDate(datetime_start) + ' ' + node)
	return datetimeNodes

def next_date(date):
	date = datetime.datetime(year(date),month(date),day(date))
	date += datetime.timedelta(days = 1)
	return str(date)[0:10]

def datetime_to_time_node(dt_start,dt_end):
	datetimeNodes = []

	if (days_diff(dt_start,dt_end) == 0):
		datetimeNodes = hour_period_to_node_with_single_date(dt_start,dt_end)
	else:
		datetimeNodes += hour_period_to_node_with_single_date(dt_start,myDate(dt_start)+' 24:00')
		for i in range(days_diff(dt_start,dt_end)-1):
			dt_start = next_date(dt_start)
			datetimeNodes += hour_period_to_node_with_single_date(dt_start+' 00:00',dt_start+' 24:00')
		datetimeNodes += hour_period_to_node_with_single_date(dt_end,myDate(dt_end)+' 24:00')

	return datetimeNodes

def days_inbetween(dt_start,dt_end):
	datetimeNodes = []

	if (days_diff(dt_start,dt_end) == 0):
		datetimeNodes.append(myDate(dt_start))
	else:
		datetimeNodes.append(myDate(dt_start))
		for i in range(days_diff(dt_start,dt_end)-1):
			dt_start = next_date(dt_start)
			datetimeNodes.append(myDate(dt_start))
	datetimeNodes.append(myDate(dt_end))
	return datetimeNodes

def string_to_datetime(dt_string):
    return datetime.datetime.strptime(dt_string,"%Y-%m-%d %H:%M:%S")

def time_node_to_datetime(time_node_array):
    time_node_array.sort()
    arraySize = len(time_node_array) - 1
    time_ranges = []
    i = 0
    while i <= arraySize :
        start_time = string_to_datetime(time_node_array[i])
        adjTime = start_time + datetime.timedelta(minutes = 30)
        if i < arraySize:
            while string_to_datetime(time_node_array[i + 1]) == adjTime:
                i += 1
                adjTime = adjTime + datetime.timedelta(minutes = 30)
                if i == arraySize:
                    break
        end_time = string_to_datetime(time_node_array[i])
        time_ranges.append(str(start_time) + ' - ' + str(end_time))
        i += 1
    return time_ranges
