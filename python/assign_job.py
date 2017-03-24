#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson, datetime_to_time_node
import re
import MySQLdb
import cgitb; cgitb.enable()

# Admin File to assign volunteers to jobs
# Takes in Event Id, JobId, Volunteer Id
# Outputs- {Success:True}, 400

form = cgi.FieldStorage()
data = {'eventId':form.getvalue("eventId"),'jobId':form.getvalue("jobId"),'volunteerId':form.getvalue("volunteerId")}
#data = {'eventId':'1','jobId':'10','volunteerId':'39'}

# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print("Database Connection failed")
	print e
	exit(1)


# Check if the input jasn value is valid
if not(data["eventId"] and data['jobId'] and data["volunteerId"]):
	print("Status: 400 Empty feilds\n")
	print("Empty feilds, vaild eventId, jobId and volunteerId must be sent")
	exit(1)

# SQL Statments
getEventSQL = "SELECT * FROM VMS_events WHERE event_id = %s"
getPersonPkSQL = "SELECT * FROM VMS_persons WHERE person_pk = %s"
getJobSQL = "SELECT job_time_start,job_time_end,person_pk FROM VMS_jobs WHERE job_id = %s"
checkTimeSQL = "SELECT job_id from VMS_volunteer_availability WHERE person_pk = %s and free_time_start = %s AND event_id = %s"
updateJobSQL = "UPDATE VMS_volunteer_availability SET job_id = %s WHERE free_time_start = %s And person_pk = %s"
addVolIDSQL = "UPDATE VMS_jobs SET person_pk = %s WHERE job_id = %s"

# Check if the event_id is valid
try:
	cursor.execute(getEventSQL,[data['eventId']])
	if cursor.rowcount < 1:
		print("Status: 400 EventId does not exist in table VMS_events\n")
		print("Invalid EventId, This event does not exist or you have entered an incorrect ID")
		exit(1)
except Exception as e:
	print("Status: 400 SQL query error (getEventSQL)\n")
	print e
	exit(1)


# Check if the volunteer_id is valid
try:
	cursor.execute(getPersonPkSQL,[data['volunteerId']])
	if cursor.rowcount < 1:
		print("Status: 400 VolunteerId does not exist in table VMS_persons\n")
		print("Invalid VolunteerId, the person does not exist or you have entered an incorrect ID")
		exit(1)
except Exception as e:
	print("Status: 400 SQL query error (getPersonPkSQL)\n")
	print e
	exit(1)

# Check if the job_id is valid
# Pull datetime info from VMS_jobs according to job_id
try:
	cursor.execute(getJobSQL,[data['jobId']])
	if cursor.rowcount < 1:
		print("Status: 400 JobId does not exist in table VMS_jobs\n")
		print("Invalid JoId, the job does not exist in VMS_jobs")
		exit(1)
	else:
		return_data = cursor.fetchall()
except Exception as e:
	print("Status: 400 SQL query error (getJobSQL)\n")
	print e
	exit(1)

##### Possible ERROR what does this do? #####
## None vs NULL or isEmpty ##
# move SQL out of execute #
if (str(return_data[0][2]) != 'None'):
	old_person_id = return_data[0][2]
	try:
		cursor.execute("UPDATE VMS_volunteer_availability SET job_id = null WHERE job_id = %s AND person_pk = %s",[data['jobId'],old_person_id])
		connection.commit()
	except Exception as e:
<<<<<<< HEAD
		print("Status: 400 SQL update error (checkTimeSQL)\n")
		print e
		exit(1)
=======
		print("Status: 400 Invalid MySQL Request\n")
		print e
		exit(1)

>>>>>>> 4f4969e059049ee410e0a1656a660d216aaa32f8

# Check if volunteer available times match job times.
# Edit to work for times not in 30min increments
for dt in datetime_to_time_node(str(return_data[0][0]),str(return_data[0][1])):
	dt += ':00'
	try:
		cursor.execute(checkTimeSQL,[data['volunteerId'],dt,data['eventId']])
		if cursor.rowcount < 1:
			print("Status: 400 volunteer availability does not match job time: some time nodes do not exist\n")
			print("volunteer availability does not match job time: some time nodes do not exist")
			exit(1)
		else:
			return_data2 = cursor.fetchall()
			if (str(return_data2[0][0]) != 'None'):
				print("Status: 400 Some of the volunteer availabilities are booked by some jobs already\n")
				print("Some of the volunteer availabilities are booked by some jobs already")
				exit(1)
	except Exception as e:
		print("Status: 400 Invalid MySQL Request(Check if volunteer availability is matching job time)\n")
		print e
		exit(1)


# Update job_id in VMS_volunteer_availability
for dt in datetime_to_time_node(str(return_data[0][0]),str(return_data[0][1])):
	dt += ':00'
	try:
		cursor.execute(updateJobSQL,[data['jobId'],dt,data['volunteerId']])
		connection.commit()
	except Exception as e:
		print("Status: 400 Invalid MySQL Request(Update job_id in VMS_volunteer_availability)\n")
		print e
		exit(1)

# Update volunteer_id in VMS_jobs
try:
	cursor.execute(addVolIDSQL,[data['volunteerId'],data['jobId']])
	connection.commit()
except Exception as e:
	print("Status: 400 Invalid MySQL Request(Update job_id in Update volunteer_id in VMS_jobs)\n")
	print e
	exit(1)


print ("Content-type: application/json")
print ("Status: 200 Login OK\n")
print sendJson({'Success':True})
