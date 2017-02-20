#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
import re
try: import simplejson as json
except ImportError: import json



#form = cgi.FieldStorage()
# Fake data:
data = {'event_name':'cwa','job_name':'drive_people_back','job_time_start':'2017-01-01 00:00:00','job_time_end':'2017-01-02 00:00:00','location':'C4C','job_description':'hahaha this is description','volunteer_needed':'5'}




# Connect to database
try:
    conn = MySQLdb.connect(user='root', passwd = '2511', db = 'cwajazz9_vms')
    c = conn.cursor()
except Exception as e:
    print("Status: Database connection initiation error")
    exit(1)



# Check if the input jason value is valid
if not(data["event_name"] and data["job_name"] and data['job_time_start'] and data['job_time_end'] and data['location'] and data['job_description'] and data['volunteer_needed']):
	print("Status: Some JSON value is empty\n")
	exit(1)
if re.match('^\d\d\d\d\-\d\d\-\d\d\s\d\d\:\d\d\:\d\d$',data["job_time_start"]) == None:
	print("Status: Invalid datetime format")
	exit(1)
if re.match('^\d\d\d\d\-\d\d\-\d\d\s\d\d\:\d\d\:\d\d$',data["job_time_end"]) == None:
	print("Status: Invalid datetime format")
	exit(1)



# Check the event_id corresponding to the event_name from table vms_events
try:
	c.execute("select event_id from vms_events where event_name = %s",[data['event_name']])
	return_id = str(c.fetchall()[0][0])
except Exception as e:
	print("Status: Event_name does not exit in table vms_events")
	exit(1)



# Insert the skill_name and skill_description into vms_skill
try:
	c.execute("insert into vms_jobs(event_id,job_name,job_time_start,job_time_end,location,job_description,volunteer_needed,volunteers_assigned)values(%s,%s,%s,%s,%s,%s,%s,%s);",[return_id,data['job_name'],data['job_time_start'],data['job_time_end'],data['location'],data['job_description'],data['volunteer_needed'],'0'])
	conn.commit()
except Exception as e:
	print("Status: Invalid MySQL Request(insert value into vms_voluteer_availability)\n")
	exit(1)



print 'Status: Successfully created job ! '












