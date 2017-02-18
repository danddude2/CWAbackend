#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi#print"Access-Control-Allow-Origin: * " #http://cwajazz.com/vms#print("Access-Control-Allow-Methods: PUT, GET, POST");#print("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
form = cgi.FieldStorage()
try: import simplejson as json
except ImportError: import json
data = { 'email':form.getvalue("email"), 'password':form.getvalue("password") }
print("Status: 200 OK\n\n")

try:
	conn = MySQLdb.connect("localhost", "cwajazz9_vms", "radio#492*", "cwajazz9_vms")
	c = conn.cursor()
	
except Exception as e:
	print("Status: 500 Server Error\n\n")
	exit(1)	
	
if data["email"] and data["password"]:
	get_pk = ("SELECT person_pk FROM person WHERE email=%s")
	get_password = ("SELECT password FROM VMS_persons WHERE person_pk=%s")
	
	try:
		c.execute(get_pk,data["email"])
		conn.commit()
		for pk in c:
			str_pk = str(pk)			
			person_pk = str_pk[1:len(str_pk)-3]
			
		c.execute(get_password,[person_pk])
		conn.commit()
		
		for p in c:
			str_p = str(p)			
			valid_password = str_p[2:len(str_p)-3]	
			
		if valid_password == data["password"]:
			out_data = { 'person_id':person_pk, 'password':valid_password,'isadmin':True }
			print("Content-type: application/json")
			print("Status: 200 OK\n\n")
			print(json.JSONEncoder().encode(out_data))
			
		else:
			print("Status: 403 Invalid Login\n\n")			
	except Exception as e:
		print("Status: 400 Invalid Request\n\n")
else:	
	print("Status: 400 Not valid\n")'''
