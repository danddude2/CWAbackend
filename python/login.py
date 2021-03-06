#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import hashlib
import MySQLdb
import cgitb; cgitb.enable()

form = cgi.FieldStorage()

data = {'email':form.getvalue("email"), 'attemptedPassword':form.getvalue("password")}
#data = {'email':'test','attemptedPassword':'test'}
output = {}

try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 500 Database Connection Error\n")
	print e
	exit(1)

getSaltSQL = "SELECT salt FROM VMS_persons WHERE person_pk =%s"
getPasswordSQL ="SELECT password FROM VMS_persons WHERE person_pk=%s"
getAdminSQL ="SELECT admin_status FROM VMS_persons WHERE person_pk=%s"
getPkSQL = "SELECT person_pk FROM VMS_persons WHERE email = %s"
getEvents = "SELECT event_id FROM VMS_volunteer_availability WHERE person_pk = %s"

try:
	cursor.execute(getPkSQL,data['email'])
	(key,) = cursor.fetchone()
	cursor.close()
except Exception as e:
	connection.rollback()
	print("Status: 401 Invalid SQL Statement\n")
	print e
	exit(1)

try:
	cursor = connection.cursor()
	cursor.execute(getSaltSQL,key)
	(s,) = cursor.fetchone()
	cursor.close()
except Exception as e:
	connection.rollback()
	print("Status: 402 Invalid SQL Statment\n")
	print e
	exit(1)

try:
	cursor = connection.cursor()
	cursor.execute(getPasswordSQL,key)
	for password in cursor:
		p=("{}".join(password))
	cursor.close()
except Exception as e:
	connection.rollback()
	print("Status: 403 Invalid SQL Statment\n")
	print e
	exit(1)

try:
	cursor = connection.cursor()
	cursor.execute(getEvents,key)
	events = []
	event_cursor = cursor.fetchall()
	for ids in event_cursor:
		[e] = ids
		events.append(e)
		events = list(set(events))
	cursor.close()
except Exception as e:
	connection.rollback()
	print("Status: 405 Invalid SQL Statment\n")
	print e
	exit(1)

#hash the password using sha512 and check if it matches stored hash
try:
	if p == hashlib.sha512(s + data['attemptedPassword']).hexdigest():
		cursor = connection.cursor()
		# get basic person info from VMS_persons
		try:
			cursor.execute('SELECT * FROM VMS_persons WHERE person_pk = %s',[key])
			if cursor.rowcount < 1:
				print("Status: 400 volunteer_id does not exist in table VMS_persons\n")
				print "Person Id does not exist"
				print '3'
			return_data = cursor.fetchall()
		except Exception as e:
			print("Status: 400 Invalid MySQL Request(check if person_id exist in VMS_persons)\n")
			print e
			exit(1)

		# Get job_id assigned to this person from VMS_jobs
		try:
			cursor.execute('SELECT job_id FROM VMS_jobs WHERE person_pk = %s',[key])
			job_ids = cursor.fetchall()
		except Exception as e:
			print("Status: 400 Invalid MySQL Request(get job_id by associated with volunteer Id)\n")
			print e
			print '1'
			exit(1)

		assigned_jobs = []
		for i in job_ids:
			assigned_jobs.append(int(i[0]))


		# Get assigned hours from VMS_availabilty
		try:
			cursor.execute('SELECT * FROM VMS_volunteer_availability WHERE person_pk = %s AND job_id IS NOT NULL',[key])
			lines = cursor.rowcount
		except Exception as e:
			print("Status: 400 Invalid MySQL Request(check if person_id exist in VMS_persons)\n")
			print e
			print'2'
			exit(1)


		info = {}
		info.update({'first_name':return_data[0][1]})
		info.update({'last_name':return_data[0][2]})
		info.update({'email':return_data[0][3]})
		info.update({'phone_number':return_data[0][5]})
		info.update({'phone_provider':return_data[0][6]})
		if return_data[0][8] == 0:
			info.update({'isAdmin':False})
		else:
			info.update({'isAdmin':True})
		info.update({'date_of_birth':return_data[0][10]})
		if return_data[0][11] == 0:
			info.update({'driver_status':False})
		else:
			info.update({'driver_status':True})
		info.update({'desired_hours':return_data[0][11]})
		info.update({'assigned_hours':lines/2.0})
		info.update({'assigned_job_ids':assigned_jobs})
		info.update({'personID':key})
		info.update({'eventIds': events})
		print"Content-type: application/json"
		print"Status: 200 Login OK"
		print ""
		print sendJson(info)
	else:
		print("Status: 400 Invalid Password\n")
except Exception as e:
	connection.rollback()
	print("Status: 406 Invalid SQL Statement\n")
	print e
	exit(1)
