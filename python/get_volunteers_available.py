#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson, string_to_datetime
import MySQLdb
import datetime
from datetime import date
import cgitb; cgitb.enable()

def person_filter(people,time_start,time_end):
<<<<<<< HEAD

=======
	
>>>>>>> 4f4969e059049ee410e0a1656a660d216aaa32f8
	# get list of people id with redundent data
	people_redun = []
	for i in people:
		people_redun.append(int(i[0]))

	# get list of people without redundent data
	people_set = list(set(people_redun))

	# calculate how many nodes are there between time start and end
	time_start = str(time_start)
	time_end = str(time_end)
	diff = (int(time_end[11:13]) - int(time_start[11:13]))*2+1
	if time_start[14:15] == '3':
		diff = diff - 1
	if time_end[14:15] == '3':
		diff = diff + 1
	# get person id with correct number of nodes and retrun list of people id
<<<<<<< HEAD
	out = []
=======
	out = [] 
>>>>>>> 4f4969e059049ee410e0a1656a660d216aaa32f8
	for i in return_data:
		if int(people_redun.count(i)) == diff:
			out.append(int(i))

	return out


form = cgi.FieldStorage()
data = {'jobId':form.getvalue("jobId")}
#data = {'jobId':7}
# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print("Database Connection failed")
	print e
	exit(1)


# Check if the input jason value is valid
if not(data["jobId"]):
	print("Status: 400 Some JSON value is empty\n")
	print("Some JSON value is empty")
	exit(1)

checkJobSQL ="SELECT * FROM VMS_jobs WHERE job_id = %s"
getJobTimeStart ="SELECT job_time_start FROM VMS_jobs WHERE job_id = %s"
getJobTimeEnd ="SELECT job_time_end FROM VMS_jobs WHERE job_id = %s"
getEventId ="SELECT event_id FROM VMS_jobs WHERE job_id = %s"
getAvailablePerson = "SELECT person_pk FROM VMS_volunteer_availability WHERE job_id IS NULL AND event_id = %s AND free_time_start BETWEEN %s AND %s"
getPersonName = "SELECT first_name,last_name FROM VMS_persons WHERE person_pk = %s"
getDesiredHours = "SELECT desired_hours FROM VMS_persons WHERE person_pk = %s"
getAssignedHours = "SELECT * FROM VMS_volunteer_availability WHERE person_pk = %s AND job_id IS NOT NULL"
# Check if the jobId_id is valid
try:
	cursor.execute(checkJobSQL,[data['jobId']])
	if cursor.rowcount < 1:
		print("Status: 400 job_id does not exist in table VMS_jobs\n")
		print("job_id does not exist in table VMS_jobs")
		exit(1)
except Exception as e:
	print("Status: 400 Invalid MySQL Request(check if job_id exist in VMS_jobs)\n")
	print e
	exit(1)

try:
	cursor.execute(getEventId,[data['jobId']])
	(eventId,) = cursor.fetchone()
except Exception as e:
	print("Status: 400 Invalid MySQL Request(Could not eventId from job_id)\n")
	print("Invalid MySQL Request(Get eventId from job_id)")
	print e
	exit(1)
# Get all volunteers with available times according to the job
try:
	cursor.execute(getJobTimeStart,[data['jobId']])
	(time_start,) = cursor.fetchone()
except Exception as e:
	print("Status: 400 Invalid MySQL Request(Could not get times from job_id)\n")
	print("Invalid MySQL Request(Get times from job_id)")
	print e
	exit(1)

try:
	cursor.execute(getJobTimeEnd,[data['jobId']])
	(time_end,) = cursor.fetchone()
	dt_end = time_end
	dt_end = dt_end - datetime.timedelta(minutes = 30)
	time_end = dt_end.strftime("%Y-%m-%d %H:%M:%S")
except Exception as e:
	print("Status: 400 Invalid MySQL Request(Could not get times from job_id)\n")
	print("Invalid MySQL Request(Get times from job_id)")
	print e
	exit(1)

try:
	cursor.execute(getAvailablePerson,[eventId,time_start,time_end])
	return_data = []
	people = cursor.fetchall()
	for person in people:
		[p] = person
		return_data.append(p)
		return_data = list(set(return_data))
except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid MySQL Request\n")
	print("Invalid MySQL Request")
	print e
	exit(1)


final_data = person_filter(people,time_start,time_end)
out_data = {}

try:

	for person in final_data:

<<<<<<< HEAD
		# Get name
=======
		# Get name	
>>>>>>> 4f4969e059049ee410e0a1656a660d216aaa32f8
		cursor.execute(getPersonName,[person])
		(first,last,) = cursor.fetchone()
		firstlast = first + ' ' + last
		out_data[person] = {}
		out_data[person].update({'name':firstlast})

		# Get desired_hours
		try:
			cursor.execute(getDesiredHours,[person])
			desired_hours = cursor.fetchall()[0][0]
		except Exception as e:
			print("Status: 400 Invalid MySQL Request(get desired hours)\n")
			print e
			exit(1)
		if desired_hours == None:
			desired_hours = 0.0
		out_data[person].update({'desired_hours':desired_hours})

		# Get assigned_hours
		try:
			cursor.execute(getAssignedHours,[person])
			lines = cursor.rowcount
		except Exception as e:
			print("Status: 400 Invalid MySQL Request(check if person_id exist in VMS_persons)\n")
			print e
			exit(1)
		out_data[person].update({'assigned_hours':lines/2.0})

except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid MySQL Request\n")
	print("Invalid MySQL Request")
	print e
	exit(1)


#out_data.update({"people_available":final_data,"people":return_names})
print"Content-type: application/json"
print"Status: 200 Login OK\n"
print sendJson(out_data)


