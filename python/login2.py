#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
try: import simplejson as json
except ImportError: import json

def login():
	form = cgi.FieldStorage()
	try:
			connection = MySQLdb.connect("localhost", "cwajazz9_vms", "radio#492*", "cwajazz9_vms")
			cursor = connection.cursor()
	except Exception as e:
			print("Status: 500 Server Error\n\n")
			exit(1)
	if form.has_key("email") and form.has_key("password"):
			email = form.getvalue("email")
			attemptedPassword = form.getvalue("password")
			try:
					cursor.execute("SELECT password FROM VMS_persons WHERE email=%s",[email])
					connection.commit()
					for p in cursor:
							password=("{}".join(p))
							if password == attemptedPassword:
									data = {'password':password,'isadmin':sure}
									print("Content-type: application/json")
									print("Status: 200 OK\n\n")
									print(json.JSONEncoder().encode(data))
							else:
									print("Status: 403 Invalid Login\n\n")
			except Exception as e:
					print("Status: 400 Invalid Request\n\n")
	else:
			print("Status: 400 Hi Nick\n\n")

print login()
