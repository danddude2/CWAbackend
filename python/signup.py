#!/usr/bin/python2.7
import cgi
import hashlib
import MySQLdb
from helper import connectDb, sendJson, encrypt
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
data = { 'firstName':form.getvalue("firstName"), 'lastName':form.getvalue("lastName"), 'email':form.getvalue("email"),'phone':form.getvalue("phone"), 'password':form.getvalue("password"), "phone_type":form.getvalue("phoneProvider"), "birth":form.getvalue("birth")}
#data = { 'firstName':"party", 'lastName':"now", 'email':"wow@email.com",'phone':"1234567891", 'password':"password", "phone_type":"Verison"}

try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 500 Database Connection Error\n")
	print e
	exit(1)

try:
	hashed, salt = encrypt(data['password'])
except Exception as e:
	print("Status: 400 Encryption error\n")
	print e
	exit(1)

addPersonSQL = ("INSERT INTO VMS_persons(first_name, last_name, email, password, phone, phone_type, salt, date_of_birth) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)")
checkPersonSQL = ("SELECT email FROM VMS_persons WHERE email=%s")
checkPersonValues = (data['email'])
addPersonValues = (data['firstName'],data['lastName'],data['email'], hashed, data['phone'], data['phone_type'], salt, data['birth'])

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
			connection.commit()
			print("Content-type: application/json")
			print("Status: 200 OK\n")
			print sendJson({'Sucess':True})
		except Exception as e:
			connection.rollback()
			print("Status: 400 Error Signing up\n")
			print e
			exit(1)
except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid Request\n")
	print e
