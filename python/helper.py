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
    date = str(time_node_array[0])[0:10]
    size = len(time_node_array) - 1
    nodes = []
    out_data = {}
    index = 0
    while index < size:
        while index < size and str(time_node_array[index])[0:10] == date:
            nodes.append(time_node_array[index])
            index += 1
        if index == size:
            nodes.append(time_node_array[index])
        out_data.update({str(date):timeranges(nodes)})
        date = str(time_node_array[index])[0:10]
        nodes = []
    return out_data

def timeranges(times):
    index = 0
    size = len(times)-1
    nodes = []
    while index <= size:
        half_hour_count = 0
        start_time = string_to_datetime(times[index])
        adj_time = start_time + datetime.timedelta(minutes = 30)
        while index < size and string_to_datetime(times[index + 1]) == adj_time:
            index += 1
            adj_time = adj_time + datetime.timedelta(minutes = 30)
            half_hour_count += 1
            if half_hour_count >= 3:
                break
        end_time = string_to_datetime(times[index])
        if str(end_time)[11:16] != "23:30":
            end_time = end_time + datetime.timedelta(minutes = 30)
        nodes.append(str(start_time)[11:16] + "-" + str(end_time)[11:16])
        index += 1
    return nodes
