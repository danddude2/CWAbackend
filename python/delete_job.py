#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
from helper import connectDb, sendJson
import cgitb; cgitb.enable()

# Admin File for deleting jobs
# Inputs - jobId
# Outputs - {Sucess:True}, 400

form = cgi.FieldStorage()
data = {'job_id':form.getvalue("jobId")}
#data = {'job_id':'22'}

# What is being returned
output = {}

# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print e
	exit(1)
if not(data["job_id"]):
	print("Status: 400 Request value is empty\n")
	exit(1)

# SQL
checkAssigned = "SELECT person_pk from VMS_jobs WHERE job_id = %s"
removeAssigned = "UPDATE VMS_volunteer_availability SET job_id = NULL WHERE person_pk = %s and job_id =%s"
deleteJobSQL = "DELETE FROM VMS_jobs WHERE job_id = %s"

# Get information from database
try:
	cursor.execute(checkAssigned,data['job_id'])
	if cursor.rowcount > 0:
		(personId,) = cursor.fetchone()
except Exception as e:
	print("Status: 400 Invalid SQL\n")
	print e
	exit(1)

# Try to delete a job, if it is assigned remove the assigned person
try:
	cursor.execute(deleteJobSQL,data['job_id'])
	cursor.execute(removeAssigned,[personId,data['job_id']])
	connection.commit()
	output.update({'Success':True})
	print "Content-type: application/json"
	print("Status: 200 Invalid SQL\n")
	print sendJson(output)
except Exception as e:
	cursor.rollback()
	print("Status: 400 Invalid SQL\n")
	print e
	exit(1)
