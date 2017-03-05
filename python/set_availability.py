#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson, hour_period_to_node
import re
import MySQLdb
import cgitb; cgitb.enable()

# Helper funciton
# Paser function: giant datetime object to database-format-array
# Input type: Dictionary
# Return type: Array
def giant_datetime_object_to_array(datetime_object):
	datetime = []
	for key,value in datetime_object.items():
		for period in value:
			for node in hour_period_to_node(period):
				datetime.append(key+' '+node)
	return datetime


form = cgi.FieldStorage()
data = {'eventId':form.getvalue("eventId"),'volunteerId':form.getvalue("volunteerId"),'time':form.getvalue("time")}
#data = {'eventId':'7','volunteerId':'7','time':{'2017-05-28':['00:00-08:00'],'2017-01-02':['13:00-14:00','15:00-17:30']}}

# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print("Database Connection failed")
	print e
	exit(1)


# Check if the input jason value is valid
if not(data["eventId"] and data["volunteerId"] and data['time']):
	print("Status: 400 Some JSON value is empty\n")
	print("Some JSON value is empty")
	exit(1)


getEventSQL = "SELECT * FROM VMS_events WHERE event_id = %s"
getPersonPkSQL = "SELECT * FROM VMS_persons WHERE person_pk = %s"
getAvailabilitySQL ="SELECT * FROM VMS_volunteer_availability WHERE event_id = %s and person_pk = %s and free_time_start = %s"

# Check if the event_id is valid
try:
	cursor.execute(getEventSQL,[data['eventId']])
	if cursor.rowcount < 1:
		print("Status: 400 Event_id does not exist in table VMS_events\n")
		print("Event_id does not exist in table VMS_events")
		exit(1)
except Exception as e:
	print("Status: 400 Invalid MySQL Request(check if event_id exist in VMS_events)\n")
	print e
	exit(1)


# Check if the volunteer_id is valid
try:
	cursor.execute(getPersonPkSQL,[data['volunteerId']])
	if cursor.rowcount < 1:
		print("Status: 400 volunteer_id does not exist in table VMS_persons\n")
		print("volunteer_id does not exist in table VMS_persons")
		exit(1)
except Exception as e:
	print("Status: 400 Invalid MySQL Request(check if volunteer_id exist in VMS_persons)\n")
	print e
	exit(1)


# Parse data and insert them into vms_volunteer_availability table
for datetime in giant_datetime_object_to_array(data['time']):
	try:
		cursor.execute(getAvailabilitySQL,[data['eventId'],data['volunteerId'],datetime])
		if cursor.rowcount == 0:
			add_event = ("INSERT INTO VMS_volunteer_availability(event_id,person_pk,free_time_start)values(%s,%s,%s)")
			add_event_values = ([data['eventId'],data['volunteerId'],datetime])

			try:
				cursor.execute(add_event,add_event_values)
				connection.commit()
			except Exception as e:
				connection.rollback()
				print("Status: 400 Invalid MySQL Request(insert value into VMS_volunteer_availability)\n")
				print("Invalid MySQL Request(insert value into VMS_volunteer_availability)")
				print e
				exit(1)
	except Exception as e:
		print("Status: 400 Invalid MySQL Request(check if data already exists)\n")
		print e
		exit(1)

print"Content-type: application/json"
print"Status: 200 Login OK\n"
print sendJson({"Success":True})
