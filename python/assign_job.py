#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import re
import MySQLdb
import cgitb; cgitb.enable()
import datetime
from datetime import date
from datetime_parser import datetime_period_to_node


form = cgi.FieldStorage()
data = {'eventId':form.getvalue("eventId"),'jobId':form.getvalue("jobId"),'volunteerId':form.getvalue("volunteerId")}
#data = {'eventId':'1','jobId':'5','volunteerId':'1'}


# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print("Database Connection failed")
	print e
	exit(1)


# Check if the input jason value is valid
if not(data["eventId"] and data['jobId'] and data["volunteerId"]):
	print("Status: 400 Some JSON value is empty\n")
	print("Some JSON value is empty")
	exit(1)


# Check if the event_id is valid
try:
	cursor.execute("SELECT * FROM VMS_events WHERE event_id = %s",[data['eventId']])
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
	cursor.execute("SELECT * FROM VMS_persons WHERE person_pk = %s",[data['volunteerId']])
	if cursor.rowcount < 1:
		print("Status: 400 volunteer_id does not exist in table VMS_persons\n")
		print("volunteer_id does not exist in table VMS_persons")
		exit(1)
except Exception as e:
	print("Status: 400 Invalid MySQL Request(check if volunteer_id exist in VMS_persons)\n")
	print e
	exit(1)


# Check if the job_id is valid
# Pull datetime info from VMS_jobs according to job_id
try:
	cursor.execute("SELECT job_time_start,job_time_end,person_pk FROM VMS_jobs WHERE job_id = %s",[data['jobId']])
	if cursor.rowcount < 1:
		print("Status: 400 Job_id does not exist in table VMS_events\n")
		print("Job_id does not exist in table VMS_events")
		exit(1)
	else:
		return_data = cursor.fetchall()
except Exception as e:
	print("Status: 400 Invalid MySQL Request(Pull info from VMS_jobs\n")
	print e
	exit(1)


# Check if job is already assigned to someone.
if (str(return_data[0][2]) != 'None'):
	print("Status: 400 Job is already assigned to someone, person_pk: %s\n",str(return_data[0][2]))
	print("Job is already assigned to someone, person_pk: " + str(return_data[0][2]))
	exit(1)


# Check if volunteer availability is matching job time.
for dt in datetime_period_to_node(str(return_data[0][0]),str(return_data[0][1])):
	dt += ':00'
	try:
		cursor.execute("SELECT job_id from VMS_volunteer_availability WHERE person_pk = %s and free_time_start = %s AND event_id = %s",[data['volunteerId'],dt,data['eventId']])
		if cursor.rowcount < 1:
			print("Status: 400 volunteer availability does not match job time: some time nodes do not exist\n")
			print("volunteer availability does not match job time: some time nodes do not exist")
			exit(1)
		else:
			return_data2 = cursor.fetchall()
			if (str(return_data2[0][0]) != 'None'):
				print("Status: 400 Some of the volunteer availabilities are booked by some jobs already\n")
				print("Some of the volunteer availabilities are booked by some jobs already")
				exit(1)
	except Exception as e:
		print("Status: 400 Invalid MySQL Request(Check if volunteer availability is matching job time)\n")
		print e
		exit(1)


# Update job_id in VMS_volunteer_availability
for dt in datetime_period_to_node(str(return_data[0][0]),str(return_data[0][1])):
	dt += ':00'
	try:
		cursor.execute("UPDATE VMS_volunteer_availability SET job_id = %s WHERE free_time_start = %s",[data['jobId'],dt])
		connection.commit()
	except Exception as e:
		print("Status: 400 Invalid MySQL Request(Update job_id in VMS_volunteer_availability)\n")
		print e
		exit(1)


# Update volunteer_id in VMS_jobs
try:
	cursor.execute("UPDATE VMS_jobs SET person_pk = %s WHERE job_id = %s",[data['volunteerId'],data['jobId']])
	connection.commit()
except Exception as e:
	print("Status: 400 Invalid MySQL Request(Update job_id in Update volunteer_id in VMS_jobs)\n")
	print e
	exit(1)


print ("Content-type: application/json")
print ("Status: 200 Login OK\n")
print sendJson({'Success':True})

