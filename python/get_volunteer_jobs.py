#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
from helper import connectDb, days_inbetween, sendJson
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
data = {'volunteer_id':form.getvalue("volunteerId"),'event_id':form.getvalue("eventId")}
data = {'volunteer_id':'1', 'event_id':'1'}

# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print e
	exit(1)

getEventsSQL = "SELECT * from VMS_jobs WHERE person_pk = %s AND event_id = %s"
# Get information from database
try:
	cursor.execute(getEventsSQL,[data['volunteer_id'],data['event_id']])
	return_data = cursor.fetchall()
except Exception as e:
	print("Status: 400 Invalid SQL\n")
	exit(1)

try:
	data = {}
	# Insert data into josn format
	for i in range(len(return_data)):
		job = {}
		job.update({'job_name':return_data[i][7]})
		job.update({'event_id':int(return_data[i][1])})
		job.update({'person_pk':return_data[i][2]})
		job.update({'job_time_start':str(return_data[i][3])})
		job.update({'job_time_end':str(return_data[i][4])})
		job.update({'location':return_data[i][5]})
		job.update({'job_description':return_data[i][6]})
		data.update({str(return_data[i][0]):job})
	print "Content-type: application/json"
	print("Status: 200 Invalid SQL\n")
	print ""
	print sendJson(data)
except Exception as e:
	print("Status: 400 Cannot Get Events\n")
	print e
	exit(1)
