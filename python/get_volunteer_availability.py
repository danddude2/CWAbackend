#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
from helper import connectDb, sendJson, time_node_to_datetime
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
#data = {'personId': '23','eventId':'1'}
data = {'personId':form.getvalue("personId"), 'eventId':form.getvalue("eventId")}

available_times = []

# Connect to database
try:
    cursor, connection = connectDb()
except Exception as e:
    print("Status: 400 Database Connection Error\n")
    print e
    exit(1)

getAvailableTimesSQL = "SELECT free_time_start FROM VMS_volunteer_availability WHERE person_pk = %s and event_id = %s"
getDesiredHoursSQL = "SELECT desired_hours FROM VMS_persons WHERE person_pk = %s"

# Get information from database
try:
    cursor.execute(getAvailableTimesSQL,[data['personId'],data['eventId']])
    avail = cursor.fetchall()
    for times in avail:
        (t,) = times
        t = t.strftime('%Y-%m-%d %H:%M:%S')
        available_times.append(t)
except Exception as e:
    print("Status: 400 Invalid SQL\n")
    print e
    exit(1)
	
try:
    cursor.execute(getDesiredHoursSQL,[data['personId']])
    (desired_hours,) = cursor.fetchone()
    
except Exception as e:
    print("Status: 400 Invalid SQL\n")
    print e
    exit(1)	

try:
    timeRange = time_node_to_datetime(available_times)
    out_data = {"availableTimes": timeRange,"desiredHours":desired_hours}
    print "Content-type: application/json"
    print("Status: 200 OK\n")
    print sendJson(out_data)
except Exception as e:
	print("Status: 400 Cannot Get Times\n")
	print e
	exit(1)
