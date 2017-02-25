#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import hashlib
import MySQLdb
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
email = form.getvalue("email")
attemptedPassword = form.getvalue("password")
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
getPkSQL = "SELECT person_pk from person WHERE email = %s"

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
	if p == hashlib.sha512(s + attemptedPassword).hexdigest():
		cursor = connection.cursor()
		cursor.execute(getAdminSQL,key)
		(status,) = cursor.fetchone()
		if(status == 0):
			data.update({'isAdmin':False})
		else:
			data.update({'isAdmin':True})
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
