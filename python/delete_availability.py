#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson, hour_period_to_node
import MySQLdb
import cgitb; cgitb.enable()

# Volunteer Side file Allows deletion of available times
# Inputs - eventId,volunteerId,date,timerange

form = cgi.FieldStorage()
data = {'eventId':form.getvalue("eventId"),'volunteerId':form.getvalue("volunteerId"),'date':form.getvalue("date"),'time':form.getvalue("time")}
#data = {'eventId':'1','volunteerId':'5','date':'2017-04-03','time':'07:30-08:30'}

# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print e
	exit(1)

# Check if the input json value is valid
if not(data['eventId'] and data['volunteerId'] and data['date'] and data['time']):
	print("Status: 400 Some JSON value is empty\n")
	print("Feilds are not all filled")
	exit(1)

# Delete data
datetimenode = []
for node in hour_period_to_node(data['time']):
	datetimenode.append(data['date']+' '+node+':00')

# SQL
deletSQL = 'DELETE FROM VMS_volunteer_availability WHERE event_id = %s and person_pk = %s and free_time_start = %s'
isAssingedSQL ='SELECT job_id from VMS_volunteer_availability WHERE event_id = %s and person_pk = %s and free_time_start = %s'

# Check if each node is already assigned if not delete
for node in datetimenode:
	try:
		cursor.execute(isAssingedSQL,[data['eventId'],data['volunteerId'],node])
		if cursor.rowcount < 1:
				print("Status: 400 Some data you want to delete does not exist in table VMS_volunteer_availability\n")
				print "Some data you want to delete does not exist in table VMS_volunteer_availability"
				exit(1)
		(jobId,) = cursor.fetchone()
		if jobId == None:
			cursor.execute(deletSQL,[data['eventId'],data['volunteerId'],node])
	except Exception as e:
		print("Status: 400 Invalid MySQL Request(delete data)\n")
		print e
		exit(1)

connection.commit()
connection.close()

print"Content-type: application/json"
print"Status: 200 Login OK\n"
print sendJson({"Success":True})
