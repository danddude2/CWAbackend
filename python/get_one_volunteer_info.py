#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import MySQLdb
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
#data = {'volunteer_id':form.getvalue("volunteerId")}
data = {'volunteer_id':'5'}

# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print e
	exit(1)

# Check if the input jason value is valid
if not(data["volunteer_id"]):
	print("Status: 400 Some JSON value is empty\n")
	print("Feilds are not all filled")
	exit(1)

# get basic person info from VMS_persons
try:
	cursor.execute('SELECT * FROM VMS_persons WHERE person_pk = %s',[data['volunteer_id']])
	if cursor.rowcount < 1:
		print("Status: 400 volunteer_id does not exist in table VMS_persons\n")
		print "Person Id does not exist"
	return_data = cursor.fetchall()
except Exception as e:
	print("Status: 400 Invalid MySQL Request(check if person_id exist in VMS_persons)\n")
	print e
	exit(1)

# Get job_id assigned to this person from VMS_jobs
try:
	cursor.execute('SELECT job_id FROM VMS_jobs WHERE person_pk = %s',data['volunteer_id'])
	job_ids = cursor.fetchall()
except Exception as e:
	print("Status: 400 Invalid MySQL Request(get job_id by associated with volunteer Id)\n")
	print e
	exit(1)

assigned_jobs = []
for i in job_ids:
	assigned_jobs.append(int(i[0]))


# Get assigned hours from VMS_availabilty
try:
	cursor.execute('SELECT * FROM VMS_volunteer_availability WHERE person_pk = %s AND job_id IS NOT NULL',[data['volunteer_id']])
	lines = cursor.rowcount
except Exception as e:
	print("Status: 400 Invalid MySQL Request(check if person_id exist in VMS_persons)\n")
	print e
	exit(1)


info = {}
info.update({'first_name':return_data[0][1]})
info.update({'last_name':return_data[0][2]})
info.update({'email':return_data[0][3]})
info.update({'phone_number':return_data[0][5]})
info.update({'phone_provider':return_data[0][6]})
if return_data[0][8] == 0:
	info.update({'admin_status':'false'})
else:
	info.update({'admin_status':'true'})
info.update({'date_of_birth':return_data[0][10]})
if return_data[0][11] == 0:
	info.update({'driver_status':'false'})
else:
	info.update({'driver_status':'true'})
info.update({'desired_hours':return_data[0][11]})
info.update({'assigned_hours':lines/2.0})
info.update({'assigned_job_ids':assigned_jobs})


print("Content-type: application/json")
print("Status: 200 OK\n")
print sendJson(info)














