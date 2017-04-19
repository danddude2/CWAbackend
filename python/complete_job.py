#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson, hour_period_to_node
import re
import MySQLdb
import cgitb; cgitb.enable()

# Not currently in use
# Volunteer file to mark a job as complete
# Inputs - EventId, jobId
# Outputs - {job_status:confirmed}

form = cgi.FieldStorage()
data = {'eventId':form.getvalue("eventId"),'jobId':form.getvalue("jobId")}
#data = {'eventId':'1','jobId':'10'}

# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print("Database Connection failed")
	print e
	exit(1)

# Check if the input jason value is valid
if not(data["eventId"] and data["jobId"]):
	print("Status: 400 Empty From values\n")
	print("Feilds are not all filled")
	exit(1)

# Check if the event_id is valid
# Move SQL out of execute
try:
	cursor.execute("SELECT * FROM VMS_events WHERE event_id = %s",[data['eventId']])
	if cursor.rowcount < 1:
		print("Status: 400 EventId does not exist in table VMS_events\n")
		print("Event_id does not exist in table VMS_events")
		exit(1)
except Exception as e:
	print("Status: 400 Invalid MySQL Request(SelectEventsSQL)\n")
	print e
	exit(1)

# Check if the job_id is valid
try:
	cursor.execute("SELECT * FROM VMS_jobs WHERE job_id = %s",[data['jobId']])
	if cursor.rowcount < 1:
		print("Status: 400 jobId does not exist in table VMS_jobs\n")
		print("job_id does not exist in table VMS_jobs")
		exit(1)
except Exception as e:
	print("Status: 400 Invalid MySQL Request(Check Job SQL)\n")
	print e
	exit(1)

# Check if the status of the job is confirmed or completed
try:
	cursor.execute("SELECT status FROM VMS_jobs WHERE job_id = %s AND event_id = %s",[data['jobId'],data['eventId']])
	status = cursor.fetchall()[0][0]
except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid MySQL Request\n")
	print("Invalid MySQL Request")
	print e
	exit(1)

out_data = {}

# Set status
# Move SQL out of executes
if status == 'confirmed':
	try:
		cursor.execute("UPDATE VMS_jobs SET status = %s WHERE job_id = %s AND event_id = %s",['completed',data['jobId'],data['eventId']])
		connection.commit()
	except Exception as e:
		connection.rollback()
		print("Status: 400 Invalid MySQL Request\n")
		print("Invalid MySQL Request")
		print e
		exit(1)
	out_data.update({'job_status':'completed'})
elif status == 'completed':
	try:
		cursor.execute("UPDATE VMS_jobs SET status = %s WHERE job_id = %s AND event_id = %s",['confirmed',data['jobId'],data['eventId']])
		connection.commit()
	except Exception as e:
		connection.rollback()
		print("Status: 400 Invalid MySQL Request\n")
		print("Invalid MySQL Request")
		print e
		exit(1)
	out_data.update({'job_status':'confirmed'})
else: out_data.update({'job_status':None})

print"Status: 200 Login OK"
print"Content-type: application/json\n"
print sendJson(out_data)
