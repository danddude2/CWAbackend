#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson, datetime_to_time_node
import re
import MySQLdb
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
# Example input
#data = {'eventId':'1','jobId':'10','volunteerId':'39'}
data = {'jobId':form.getvalue("jobId"),'volunteerId':form.getvalue("volunteerId")}

# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 500 Database Connection Error\n")
	print("Database Connection failed")
	print e
	exit(1)

# Check if the input json value is valid
if not(data['jobId'] and data["volunteerId"]):
	print("Status: 400 One or more input values empty\n")
	print("Json input value is empty")
	exit(1)

getPersonPkSQL = "SELECT * FROM VMS_persons WHERE person_pk = %s"
getJobSQL = "SELECT * FROM VMS_jobs WHERE job_id = %s"
updateJobSQL = "UPDATE VMS_volunteer_availability SET job_id = NULL WHERE job_id = %s and person_pk = %s"
removeVolIDSQL = "UPDATE VMS_jobs SET person_pk = NULL WHERE job_id = %s"

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


# Check if the job_id is valid
# Pull datetime info from VMS_jobs according to job_id
try:
	cursor.execute(getJobSQL,[data['jobId']])
	if cursor.rowcount < 1:
		print("Status: 400 Job_id does not exist in table VMS_events\n")
		print("Job_id does not exist in table VMS_events")
		exit(1)
except Exception as e:
	print("Status: 400 Invalid MySQL Request(Pull info from VMS_jobs\n")
	print e
	exit(1)

# remove the assignment form the DB
try:
	cursor.execute(updateJobSQL,[data['jobId'],data['volunteerId']])
	cursor.execute(removeVolIDSQL,[data['jobId']])
	connection.commit()
except Exception as e:
	print("Status: 400 Invalid MySQL Request(Update job_id in VMS_volunteer_availability)\n")
	print e
	exit(1)

print ("Content-type: application/json")
print ("Status: 200 Login OK\n")
print sendJson({'Success':True})
