#!/usr/bin/python2.7
import cgi
import hashlib
import MySQLdb
from helper import connectDb, sendJson, encrypt
import cgitb; cgitb.enable()
form = cgi.FieldStorage()

data = { "person_pk":form.getvalue("volunteerId"), "admin":form.getvalue("admin"), "driver":form.getvalue("driver")}
#data = { "person_pk":"5", "admin":"False", "driver":"False"}

try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 500 Database Connection Error\n")
	print e
	exit(1)

adminPersonSQL = ("UPDATE VMS_persons SET admin_status=%s WHERE person_pk = %s")
driverPersonSQL = ("UPDATE VMS_persons SET driver_status=%s WHERE person_pk = %s")
# this maybe closer to that of the admin field, we will see 

if data['admin'] == "true": data['admin'] = True
else :data['admin'] = False

if data['driver'] == "true": data['driver'] = True
else :data['driver'] = False

adminPersonValues = (data['admin'],data['person_pk'])
driverPersonValues = (data['driver'],data['person_pk'])

try:
	
	try:
		#if data['admin']:
		cursor = connection.cursor()
		cursor.execute(adminPersonSQL,adminPersonValues)
		connection.commit()
		cursor.close()
		
	except Exception as e:
		connection.rollback()
		print("Status: 400 Error Setting as admin\n")
		print e
		exit(1)
		
	try:
		#if data['driver']:
		cursor = connection.cursor()
		cursor.execute(driverPersonSQL,driverPersonValues)
		connection.commit()
		cursor.close()
			
	except Exception as e:
		connection.rollback()
		print("Status: 400 Error settings as driver\n")
		print e
		exit(1)
		
except Exception as e:
	connection.rollback()
	print("Status: 400 Invalid Request\n")
	print e
	
print("Content-type: application/json")
print("Status: 200 OK\n")
print sendJson({'Sucess':True})
