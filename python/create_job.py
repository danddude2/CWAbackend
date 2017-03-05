#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import re
import MySQLdb
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
data = { 'event_id':form.getvalue("eventId"), 'job_name':form.getvalue("jobName"), "job_date":form.getvalue("jobDate"), "job_time_start":form.getvalue("startTime"), 'job_time_end':form.getvalue("endTime"), 'location':form.getvalue("location"), 'job_description':form.getvalue("jobDesciption")}
#data = {'event_id':'7','job_name':'Make balloons','job_time_start':'2017-05-28 07:00:00','job_time_end':'2017-05-28 08:00:00','location':'C4C','job_description':'Make animals out of rubber'}

data['job_time_start'] = str(data['job_date']) + ' ' + str(data['job_time_start'])
data['job_time_end'] = str(data['job_date']) + ' ' + str(data['job_time_end'])
# Connect to database
try:
    cursor, connection = connectDb()
except Exception as e:
    print("Status: 400 Database Connection Error\n")
    print e
    exit(1)

# Check if the input jason value is valid
if not(data["event_id"] and data["job_name"] and data['job_time_start'] and data['job_time_end'] and data['location'] and data['job_description']):
    print("Status: 400 Some JSON value is empty\n")
    print("Feilds are not all filled")
    exit(1)
if re.match('^\d\d\d\d\-\d\d\-\d\d\s\d\d\:\d\d\:\d\d$',data["job_time_start"]) == None:
    print("Status: 400 \Invalid datetime format\n")
    exit(1)
if re.match('^\d\d\d\d\-\d\d\-\d\d\s\d\d\:\d\d\:\d\d$',data["job_time_end"]) == None:
    print("Status: 400 Invalid datetime format\n")
    exit(1)

checkEventId = "SELECT * FROM VMS_events WHERE event_id = %s"
insertJob = "INSERT INTO VMS_jobs(event_id,job_name,job_time_start,job_time_end,location,job_description)values(%s,%s,%s,%s,%s,%s);"

# Check if the event_id is valid
try:
    cursor.execute(checkEventId,[data['event_id']])
    if cursor.rowcount < 1:
        print("Status: 400 Event_id does not exist in table VMS_events\n")
        exit(1)
except Exception as e:
    print("Status: 400 Invalid MySQL Request(check if event_id exist in VMS_events)\n")
    print e
    exit(1)

# Insert the skill_name and skill_description into vms_skill
try:
    cursor.execute(insertJob,[data['event_id'],data['job_name'],data['job_time_start'],data['job_time_end'],data['location'],data['job_description']])
    connection.commit()
    print"Content-type: application/json"
    print"Status: 200 Login OK\n"
    print sendJson({'Success':True})
except Exception as e:
    connection.rollback()
    print("Status: 400 Invalid MySQL Request(insert value into VMS_jobs)\n")
    print e
    exit(1)
