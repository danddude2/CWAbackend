#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import MySQLdb
import cgitb; cgitb.enable()

form = cgi.FieldStorage()

data = { 'eventname':form.getvalue("eventName"), 'startdate':form.getvalue("startDate"), 'enddate':form.getvalue("endDate")}


try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 500 Database Connection Error\n")
	print e
	exit(1)
	
add_event = ("INSERT INTO VMS_events (event_name,start_date,end_date) VALUES (%s,%s,%s)") #start_date,end_date
add_event_values = (data['eventname'],data['startdate'],data['enddate'])
check_event = ("SELECT event_id FROM VMS_events WHERE event_name=%s")

try:
	cursor.execute(check_event,data['eventname'])
	rowcount = cursor.rowcount	
	cursor.close()

except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid SQL Command\n")
	print e
	exit(1) 
	
try:
	if rowcount == 0:
		cursor = connection.cursor()
		cursor.execute(add_event, add_event_values)
		connection.commit()
		cursor.close()
		print("Status: 200 Event created\n")
	else:
		print("Status: 400 Event already in database\n")
		exit(1)
	
except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid SQL Statment\n")
	print e
	exit(1)

print("Status: 201 Event made\n")

