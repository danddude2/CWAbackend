#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
import re
try: import simplejson as json
except ImportError: import json




#form = cgi.FieldStorage()
# Fake data:
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



# Return the information corresponding to the input event_id in table vms_events
try:
	c.execute("select * from vms_events where event_id = %s",[data['event_id']])
	return_data = c.fetchall()
except Exception as e:
	print("Status: Invalid MySQL Request(pull data from vms_events with event_id")
	exit(1)



# Insert data into josn format
out_data = {}
out_data.update({'event_name':return_data[0][1]})
out_data.update({'event_description':return_data[0][2]})



print out_data





