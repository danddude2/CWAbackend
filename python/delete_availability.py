#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson, hour_period_to_node
import MySQLdb
import cgitb; cgitb.enable()


form = cgi.FieldStorage()
data = {'eventId':form.getvalue("eventId"),'volunteerId':form.getvalue("volunteerId"),'date':form.getvalue("date"),'time':form.getvalue("time")}
#data = {'eventId':'2','volunteerId':'3','date':'2017-03-06','time':'05:30-06:00'}


# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print e
	exit(1)


# Check if the input jason value is valid
if not(data['eventId'] and data['volunteerId'] and data['date'] and data['time']):
	print("Status: 400 Some JSON value is empty\n")
	print("Feilds are not all filled")
	exit(1)


# Delete data
datetimenode = []
for node in hour_period_to_node(data['time']):
	datetimenode.append(data['date']+' '+node+':00')

deletSQL = 'DELETE FROM VMS_volunteer_availability WHERE event_id = %s and person_pk = %s and free_time_start = %s'

for node in datetimenode:
	try:
		cursor.execute(deletSQL,[data['eventId'],data['volunteerId'],node])
		if cursor.rowcount < 1:
			print("Status: 400 Some data you want to delete does not exist in table VMS_volunteer_availability\n")
			print "Some data you want to delete does not exist in table VMS_volunteer_availability"
			exit(1)
	except Exception as e:
		print("Status: 400 Invalid MySQL Request(delete data)\n")
		print e
		exit(1)

connection.commit()
connection.close()


print"Content-type: application/json"
print"Status: 200 Login OK\n"
print sendJson({"Success":True})





