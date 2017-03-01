#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import hashlib
import MySQLdb
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
email = form.getvalue("email")
attemptedPassword = form.getvalue("password")
#email = "volunteer"
#attemptedPassword = "root"
data = {}

try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 500 Database Connection Error\n")
	print e
	exit(1)

getSaltSQL = "SELECT salt FROM VMS_persons WHERE person_pk =%s"
getPasswordSQL ="SELECT password FROM VMS_persons WHERE person_pk=%s"
getAdminSQL ="SELECT admin_status FROM VMS_persons WHERE person_pk=%s"
getPkSQL = "SELECT person_pk FROM person WHERE email = %s"
getEvents = "SELECT event_id FROM VMS_voluteer_availability WHERE person_pk = %s"

try:
	cursor.execute(getPkSQL,[email])
	(key,) = cursor.fetchone()
	cursor.close()
except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid SQL Statement\n")
	print e
	exit(1)

try:
	cursor = connection.cursor()
	cursor.execute(getSaltSQL,key)
	(s,) = cursor.fetchone()
	cursor.close()
except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid SQL Statment\n")
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
	print("Status: 400 Invalid SQL Statment\n")
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
	print("Status: 400 Invalid SQL Statment\n")
	print e
	exit(1)

try:
	if p == hashlib.sha512(s + attemptedPassword).hexdigest():
		cursor = connection.cursor()
		cursor.execute(getAdminSQL,key)
		(status,) = cursor.fetchone()
		if(status == 0):
			data.update({'isAdmin':False,'personID':key, 'eventIds':events})
		else:
			data.update({'isAdmin':True,'personID':key, 'eventIds':events})
		print"Content-type: application/json"
		print"Status: 200 Login OK"
		print ""
		print sendJson(data)
	else:
		print("Status: 400 Invalid Password\n")
except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid SQL Statement\n")
	print e
	exit(1)
