#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import MySQLdb
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
# Fake data:
#data = {'job_id':'4'}
data ={ 'job_id':form.getvalue('jobId')}
# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 500 Database Connection Error\n")
	print e
	exit(1)

# Check if the input jason value is valid
if not(data["job_id"]):
	print("Status: 400 Some JSON value is empty\n")
	exit(1)


getJobInfo = "SELECT * FROM VMS_jobs WHERE job_id = %s"
# Return the information corresponding to the input job_name in table vms_jobs
try:
	cursor.execute(getJobInfo,[data['job_id']])
	return_data = cursor.fetchall()
except Exception as e:
	print("Status: 400 Invalid MySQL Request(pull data from VMS_jobs with event_id\n")
	print e
	exit(1)

try:
	# Insert data into josn format
	out_data = {}
	for i in range(len(return_data)):
		job = {}
		job.update({'event_id':int(return_data[i][1])})
		job.update({'person_pk':return_data[i][2]})
		job.update({'job_time_start':str(return_data[i][3])})
		job.update({'job_time_end':str(return_data[i][4])})
		job.update({'location':return_data[i][5]})
		job.update({'job_description':return_data[i][6]})
		job.update({'job_name':return_data[i][7]})
		job.update({'job_status':return_data[i][8]})

		out_data.update({str(return_data[i][0]):job})
	print("Content-type: application/json")
	print("Status: 200 OK\n")
	print sendJson(out_data)
except Exception as e:
	print("Status: 500 Database Connection Error\n")
	print e
	exit(1)
