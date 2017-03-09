#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import MySQLdb
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
data = {'jobId':form.getvalue("jobId")}
#data = {'jobId':12}
# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print("Database Connection failed")
	print e
	exit(1)


# Check if the input jason value is valid
if not(data["jobId"]):
	print("Status: 400 Some JSON value is empty\n")
	print("Some JSON value is empty")
	exit(1)

checkJobSQL ="SELECT * FROM VMS_jobs WHERE job_id = %s"
getJobTimeStart ="SELECT job_time_start FROM VMS_jobs WHERE job_id = %s"
getJobTimeEnd ="SELECT job_time_end FROM VMS_jobs WHERE job_id = %s"
getEventId ="SELECT event_id FROM VMS_jobs WHERE job_id = %s"
getAvailablePerson = "SELECT person_pk FROM VMS_volunteer_availability WHERE job_id IS NULL AND event_id = %s AND free_time_start BETWEEN %s AND %s"
# Check if the jobId_id is valid
try:
	cursor.execute(checkJobSQL,[data['jobId']])
	if cursor.rowcount < 1:
		print("Status: 400 Event_id does not exist in table VMS_events\n")
		print("Event_id does not exist in table VMS_events")
		exit(1)
except Exception as e:
	print("Status: 400 Invalid MySQL Request(check if event_id exist in VMS_events)\n")
	print e
	exit(1)


try:
	cursor.execute(getEventId,[data['jobId']])
	(eventId,) = cursor.fetchone()
except Exception as e:
	print("Status: 400 Invalid MySQL Request(Could not eventId from job_id)\n")
	print("Invalid MySQL Request(Get eventId from job_id)")
	print e
	exit(1)


# Get all volunteers with available times according to the job
try:
	cursor.execute(getJobTimeStart,[data['jobId']])
	(time_start,) = cursor.fetchone()
except Exception as e:
	print("Status: 400 Invalid MySQL Request(Could not get times from job_id)\n")
	print("Invalid MySQL Request(Get times from job_id)")
	print e
	exit(1)

try:
	cursor.execute(getJobTimeEnd,[data['jobId']])
	(time_end,) = cursor.fetchone()
except Exception as e:
	print("Status: 400 Invalid MySQL Request(Could not get times from job_id)\n")
	print("Invalid MySQL Request(Get times from job_id)")
	print e
	exit(1)

try:
	cursor.execute(getAvailablePerson,[eventId,time_start,time_end])
	return_data = []
	people = cursor.fetchall()
	for person in people:
		[p] = person
		return_data.append(p)
		return_data = list(set(return_data))
except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid MySQL Request(insert value into VMS_voluteer_availability)\n")
	print("Invalid MySQL Request(insert value into VMS_voluteer_availability)")
	print e
	exit(1)

out_data = {}
out_data.update({"people_available":return_data})
print"Content-type: application/json"
print"Status: 200 Login OK\n"
print sendJson(out_data)
