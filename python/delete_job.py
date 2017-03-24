#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
from helper import connectDb, sendJson
import cgitb; cgitb.enable()

form = cgi.FieldStorage()

data = {'job_id':form.getvalue("jobId")}
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

try:
	cursor.execute(deleteJobSQL,data['job_id'])
	cursor.execute(removeAssigned,[personId,data['job_id']])
	output.update({'Success':True})
	print "Content-type: application/json"
	print("Status: 200 Invalid SQL\n")
	print sendJson(output)
except Exception as e:
	cursor.rollback()
	print("Status: 400 Invalid SQL\n")
	print e
	exit(1)
