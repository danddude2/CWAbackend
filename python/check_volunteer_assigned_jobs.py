#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import MySQLdb
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
data = {'personId':form.getvalue("personId"), 'eventId':form.getvalue("eventId")}
#data = {'personId':14816,'eventId':1}
# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print("Database Connection failed")
	print e
	exit(1)


# Check if the input jason value is valid
if not(data["personId"] and data["eventId"]):
	print("Status: 400 Some JSON value is empty\n")
	print("Some JSON value is empty")
	exit(1)

# Check if the jobId_id is valid
try:
	cursor.execute("SELECT * FROM VMS_persons WHERE person_pk = %s",[data['personId']])
	if cursor.rowcount < 1:
		print("Status: 400 Person_id does not exist in table VMS_persons\n")
		print("persons_id does not exist in table VMS_persons")
		exit(1)
except Exception as e:
	print("Status: 400 Invalid MySQL Request(check if persons exist in VMS_persons)\n")
	print e
	exit(1)

# Check if they have alreay signed up
try:
	cursor.execute("SELECT * FROM VMS_voluteer_availability WHERE person_pk = %s",[data['personId']])
	if cursor.rowcount < 1:
        	print"Content-type: application/json"
        	print"Status: 200 OK\n"
        	print sendJson({"my_jobs":'',"availability_check":False})
        	exit(1)
except Exception as e:
	print("Status: 400 Invalid MySQL Request(check if person exist in VMS_voluteer_availability)\n")
	print e
	exit(1)

# Get all volunteers with available times according to the job
try:
	cursor.execute("SELECT * FROM VMS_job_assignments WHERE person_pk = %s",[data['personId']])
	return_data = []
	jobs = cursor.fetchall()
	for job in jobs:
		[j] = job
		return_data.append(j)
		return_data = list(set(return_data))
except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid MySQL Request(insert value into VMS_voluteer_availability)\n")
	print("Invalid MySQL Request(insert value into VMS_voluteer_availability)")
	print e
	exit(1)

out_data = {}
out_data.update({"jobs_assigned":return_data})
out_data.update({"availability_check":True})
print"Content-type: application/json"
print"Status: 200 Login OK\n"
print sendJson(out_data)