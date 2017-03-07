#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import MySQLdb
import cgitb; cgitb.enable()


form = cgi.FieldStorage()
data = {'volunteerId':form.getvalue("volunteerId")}
#data = {'volunteerId':'1'}


# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print e
	exit(1)


# Check if the input jason value is valid
if not(data["volunteerId"]):
	print("Status: 400 Some JSON value is empty\n")
	print("Feilds are not all filled")
	exit(1)


# Get data from VMS_volunteer_availability
try:
	cursor.execute("SELECT event_id FROM VMS_volunteer_availability WHERE person_pk = %s",[data['volunteerId']])
	return_data = cursor.fetchall()
	if cursor.rowcount < 1:
		print("Status: 400 Data does not exist in table VMS_volunteer_availability\n")
		print "Data does not exist"
except Exception as e:
	print("Status: 400 Invalid MySQL Request(check if event_id exist in VMS_event)\n")
	print e
	exit(1)

out_data_array = []
pre_item = 0
for item in return_data:
	if int(item[0]) != pre_item:
		out_data_array.append(int(item[0]))
	pre_item = int(item[0])
out_data = {'eventId':out_data_array}


print("Content-type: application/json")
print("Status: 200 OK\n")
print sendJson(out_data)




