#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
import re
try: import simplejson as json
except ImportError: import json




#form = cgi.FieldStorage()
# Fake data:
data = {'job_name':'drive_people_back'}




# Connect to database
try:
    conn = MySQLdb.connect(user='root', passwd = '2511', db = 'cwajazz9_vms')
    c = conn.cursor()
except Exception as e:
    print("Status: Database connection initiation error")
    exit(1)



# Check if the input jason value is valid
if not(data["job_name"]):
	print("Status: Some JSON value is empty\n")
	exit(1)



# Check if the job_name already exist in VMS_jobs and find the corresponding job_id
try:
	c.execute("select job_id from vms_jobs where job_name = %s",[data['job_name']])
	if c.rowcount == 0:
		print("Status: job_name does not exist in VMS_jobs")
		exit(1)
except Exception as e:
	print("Status: Invalid MySQL Request(check job_id duplication")
	exit(1)



# Return the information corresponding to the input job_name in table vms_jobs
try:
	c.execute("select job_id,event_id,job_time_start,job_time_end,location,job_description,volunteer_needed,volunteers_assigned from vms_jobs where job_name = %s",[data['job_name']])
	return_data = c.fetchall()
except Exception as e:
	print("Status: Invalid MySQL Request(pull data from vms_jobs with job_name")
	exit(1)



# Insert data into josn format
out_data = {}
for i in range(len(return_data)):
	out_data.update({"job_id"+str(i):int(return_data[i][0])})
	out_data.update({"event_id"+str(i):return_data[i][1]})
	out_data.update({"job_time_start"+str(i):str(return_data[i][2])})
	out_data.update({"job_time_end"+str(i):str(return_data[i][3])})
	out_data.update({"location"+str(i):return_data[i][4]})
	out_data.update({"job_description"+str(i):return_data[i][5]})
	out_data.update({"volunteer_needed"+str(i):return_data[i][6]})
	out_data.update({"volunteers_assigned"+str(i):return_data[i][7]})


print out_data








