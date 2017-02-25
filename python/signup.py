#!/usr/bin/python2.7
import cgi
import hashlib
import MySQLdb
from helper import connectDb, sendJson, encrypt
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
data = { 'firstName':form.getvalue("firstName"), 'lastName':form.getvalue("lastName"), 'email':form.getvalue("email"),'phone':form.getvalue("phone"), 'password':form.getvalue("password"), "phone_type":form.getvalue("phoneProvider")}

try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 500 Database Connection Error\n")
	print e
	exit(1)

addPersonSQL = ("INSERT INTO person(name_first,name_last,email,phone_mobile) VALUES(%s,%s,%s,%s)")
checkPersonSQL = ("SELECT email FROM person WHERE email=%s")
addPasswordSQL = ("INSERT INTO VMS_persons(person_pk,password,salt,phone_type) VALUES(%s,%s,%s,%s)")

addPersonValues = (data['firstName'],data['lastName'],data['email'],data['phone'])
checkPersonValues = (data['email'])

try:
	cursor.execute(checkPersonSQL,checkPersonValues)
	if cursor.rowcount != 0:
		print("Status: 420 Email Already Exist\n")
		exit(1)
	else:
		cursor.close()
		try:
			cursor = connection.cursor()
			cursor.execute(addPersonSQL,addPersonValues)

			personPk = cursor.lastrowid
			hashed, salt = encrypt(data['password'])
			addPasswordValues = (personPk,hashed,salt,data['phone_type'])

			cursor.execute(addPasswordSQL,addPasswordValues)
			connection.commit()
			print("Status: 200 OK\n")
		except Exception as e:
			connection.rollback()
			print("Status: 400 Error Signing up\n")
			print e
			exit(1)
except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid Request\n")
	print e
