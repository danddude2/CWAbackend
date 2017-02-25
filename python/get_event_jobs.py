#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import hashlib
import MySQLdb
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
data = {'event_id':form.getvalue("eventId")}
#data = {'event_id':'8'}

# Connect to database
try:
    cursor, connection = connectDb()
except Exception as e:
    print("Status: 400 Database Connection Error\n")
    print e
    exit(1)

# Check if the input jason value is valid
if not(data["event_id"]):
    print("Status: 400 Some JSON value is empty\n")
    print("Feilds are not all filled")
    exit(1)

# Check if the event_id is valid
try:
    cursor.execute("SELECT * FROM VMS_events WHERE event_id = %s",[data['event_id']])
    if cursor.rowcount < 1:
        print("Status: 400 Event_id does not exist in table VMS_event\n")
        print "Event Id does not exist"
except Exception as e:
    print("Status: Invalid MySQL Request(check if event_id exist in VMS_event)")
    print e
    exit(1)

# Get information from database
try:
    cursor.execute("SELECT * FROM VMS_jobs WHERE event_id = %s",[data['event_id']])
    return_data = cursor.fetchall()
except Exception as e:
    print("Status: 400 Invalid MySQL Request(pull data from VMS_jobs with event_id\n")
    print e
    exit(1)

# Insert data into josn format
out_data = {}
for i in range(len(return_data)):
    event = {}
    event.update({'event_id':int(return_data[i][1])})
    event.update({'job_skill':return_data[i][2]})
    event.update({'job_time_start':str(return_data[i][3])})
    event.update({'job_time_end':str(return_data[i][4])})
    event.update({'location':return_data[i][5]})
    event.update({'job_description':return_data[i][6]})
    event.update({'volunteer_needed':int(return_data[i][7])})
    event.update({'job_name':return_data[i][8]})
    event.update({'volunteer_assigned':int(return_data[i][9])})
    out_data.update({'job_id: '+str(return_data[i][0]):event})
print("Content-type: application/json")
print("Status: 200 OK\n")
print sendJson(out_data)
