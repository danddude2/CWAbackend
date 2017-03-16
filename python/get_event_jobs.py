#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import MySQLdb
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
data = {'event_id':form.getvalue("eventId")}
#data = {'event_id':'1'}

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

getEventIdSQL = "SELECT * FROM VMS_events WHERE event_id = %s"
getJobsSQL = "SELECT * FROM VMS_jobs WHERE event_id = %s"

# Check if the event_id is valid
try:
	cursor.execute(getEventIdSQL,[data['event_id']])
	if cursor.rowcount < 1:
		print("Status: 400 Event_id does not exist in table VMS_event\n")
		print "Event Id does not exist"
except Exception as e:
	print("Status: 400 Invalid MySQL Request(check if event_id exist in VMS_event)\n")
	print e
	exit(1)

# Get information from database
try:
	cursor.execute(getJobsSQL,[data['event_id']])
	return_data = cursor.fetchall()
except Exception as e:
	print("Status: 400 Invalid MySQL Request(pull data from VMS_jobs with event_id\n")
	print e
	exit(1)

try:
	# Insert data into josn format
	out_data = {}
	for i in range(len(return_data)):

		job_time_date = str(return_data[i][3])[0:10]
		job_time_start_hour = str(return_data[i][3])[11:16]
		job_time_end_hour = str(return_data[i][4])[11:16]
		
		event = {}
		event.update({'event_id':int(return_data[i][1])})
		event.update({'volunteer_id':return_data[i][2]})
		event.update({'first_name':None})
		event.update({'last_name':None})
		
		if return_data[i][2] != None:
			try:
				cursor.execute('SELECT first_name,last_name FROM VMS_persons WHERE person_pk = %s',[return_data[i][2]])
				volunteername = cursor.fetchall()
			except Exception as e:
				print("Status: 400 Invalid MySQL Request(pull data from VMS_jobs with event_id\n")
				print e
				exit(1)

			event['first_name'] = volunteername[0][0]
			event['last_name'] = volunteername[0][1]
		
		event.update({'job_date':job_time_date})
		event.update({'job_time_start':job_time_start_hour})
		event.update({'job_time_end':job_time_end_hour})
		event.update({'location':return_data[i][5]})
		event.update({'job_description':return_data[i][6]})
		event.update({'job_name':return_data[i][7]})
		out_data.update({str(return_data[i][0]):event})

	print("Content-type: application/json")
	print("Status: 200 OK\n")
	print sendJson(out_data)

except Exception as e:
	print("Status: 400 Could Not get Job\n")
	print e
	exit(1)
