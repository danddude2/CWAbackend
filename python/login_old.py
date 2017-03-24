#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import hashlib
import MySQLdb
import cgitb; cgitb.enable()

form = cgi.FieldStorage()

data = {'email':form.getvalue("email"), 'attemptedPassword':form.getvalue("password")}
#data = {'email':'wow@email.com','attemptedPassword':'password'}
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
		cursor.execute(getAdminSQL,key)
		(status,) = cursor.fetchone()
		if(status == 0):
			output.update({'isAdmin':False,'personID':key, 'eventIds':events})
		else:
			output.update({'isAdmin':True,'personID':key, 'eventIds':events})
		print"Content-type: application/json"
		print"Status: 200 Login OK"
		print ""
		print sendJson(output)
	else:
		print("Status: 400 Invalid Password\n")
except Exception as e:
	connection.rollback()
	print("Status: 406 Invalid SQL Statement\n")
	print e
	exit(1)
