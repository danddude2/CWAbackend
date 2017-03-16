#!/usr/bin/python2.7
import cgi
from helper import connectDb, sendJson
import MySQLdb
import cgitb; cgitb.enable()


# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 400 Database Connection Error\n")
	print e
	exit(1)


# Clear VMS_jobs
try:
    cursor.execute('SET foreign_key_checks = 0;DELETE FROM VMS_jobs where job_id < 20000000;SET foreign_key_checks = 1;ALTER TABLE VMS_jobs AUTO_INCREMENT = 1;')
    #connection.commit()
    print"Content-type: application/json"
    print"Status: 200 Login OK\n"
    print sendJson({'Success':True})
except Exception as e:
    print("Status: 400 Invalid MySQL Request(clear VMS_jobs)\n")
    print e
    exit(1)