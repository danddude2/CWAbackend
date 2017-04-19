#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import MySQLdb
import cgitb; cgitb.enable()

# Admin file for event_creation
# Events have jobs which have people assigned

form = cgi.FieldStorage()
data = { 'eventname':form.getvalue("eventName"), 'startdate':form.getvalue("startDate"), 'enddate':form.getvalue("endDate")}
#data = { 'eventname':"Party", 'startdate':'2017-05-28', 'enddate':'2017-06-03'}

# Connect to the database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print e
	exit(1)

# SQL statments
add_event = ("INSERT INTO VMS_events (event_name,start_date,end_date) VALUES (%s,%s,%s)")
add_event_values = (data['eventname'],data['startdate'],data['enddate'])
check_event = ("SELECT event_id FROM VMS_events WHERE event_name=%s")

# Get eventId from the event name
try:
	cursor.execute(check_event,data['eventname'])
	rowcount = cursor.rowcount
	cursor.close()
except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid SQL Command (check_event)\n")
	print e
	exit(1)

# If the event doesn't exist create a new one
try:
	if rowcount == 0:
		cursor = connection.cursor()
		cursor.execute(add_event, add_event_values)
		connection.commit()
		cursor.close()
		print("Status: 200 Event created\n")
		success = {'Success':True}
		print sendJson(success)
	else:
		print("Status: 400 Event already in database\n")
		exit(1)

except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid SQL Statment (add_event)\n")
	print e
	exit(1)
