#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
try: import simplejson as json
except ImportError: import json




data = {'event_id':'1'}




# Connect to database
try:
    conn = MySQLdb.connect(user='root', passwd = '2511', db = 'cwajazz9_vms')
    c = conn.cursor()
except Exception as e:
    print("Status: Database connection initiation error")
    exit(1)




# Check if the input jason value is valid
if not(data["event_id"]):
	print("Status: Some JSON value is empty\n")
	exit(1)




# Check if the event_id is valid
try:
	c.execute("select * from vms_events where event_id = %s",[data['event_id']])
	if c.rowcount < 1:
		print("Status: Event_id does not exist in table vms_event")
except Exception as e:
	print("Status: Invalid MySQL Request(check if event_id exist in vms_event)")
	exit(1)




# Get information from database
try:
	c.execute("select * from vms_jobs where event_id = %s",[data['event_id']])
	return_data = c.fetchall()
except Exception as e:
	print("Status: Invalid MySQL Request(pull data from vms_jobs with event_id")
	exit(1)




# Insert data into josn format
out_data = {}
for i in range(len(return_data)):
	event = {}
	event.update({'event_id':int(return_data[i][1])})
	event.update({'job_skill':return_data[i][2]})
	event.update({'job_time_start':return_data[i][3]})
	event.update({'job_time_end':return_data[i][4]})
	event.update({'location':return_data[i][5]})
	event.update({'job_description':return_data[i][6]})
	event.update({'volunteer_needed':int(return_data[i][7])})
	event.update({'volunteer_assigned':int(return_data[i][8])})
	out_data.update({'job_id: '+str(return_data[i][0]):event})


print out_data



