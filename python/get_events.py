#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
try: import simplejson as json
except ImportError: import json


# Connect to database
try:
    conn = MySQLdb.connect(user='root', passwd = '2511', db = 'cwajazz9_vms')
    c = conn.cursor()
except Exception as e:
    print("Status: Database connection initiation error")
    exit(1)



# Get information from database
try:
	c.execute("select * from vms_events")
	return_data = c.fetchall()
except Exception as e:
	print("Status: Invalid MySQL Request(pull data from vms_events with job_name")
	exit(1)



# Insert data into josn format
out_data = {}
for i in range(len(return_data)):
	event = {}
	event.update({'event_name':return_data[i][1]})
	event.update({'event_description':return_data[i][2]})
	out_data.update({'event_id: '+str(return_data[i][0]):event})




print out_data



