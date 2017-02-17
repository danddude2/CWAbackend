#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
#import bcrypt

form = cgi.FieldStorage()

try: import simplejson as json
except ImportError: import json

#print"Access-Control-Allow-Origin: http://cwajazz.com/vms"

data = { 'firstName':form.getvalue("firstName"), 'lastName':form.getvalue("lastName"), 'email':form.getvalue("email"),'phone':form.getvalue("phone"), 'password':form.getvalue("password"), 'phone_type':form.getvalue("phoneProvider")}

try:
    conn = MySQLdb.connect("localhost", "cwajazz9_vms", "radio#492*", "cwajazz9_vms")
    c = conn.cursor()
    
except Exception as e:
    print("Status: 503 Server Error\n")
    exit(1)
    
if data["firstName"] and data["lastName"] and data["email"] and data["phone"] and data["password"]:
  
    add_person = ("INSERT INTO person(name_first,name_last,email,phone_mobile) VALUES(%s,%s,%s,%s)")
    check_person =  ("SELECT email FROM person WHERE email=%s")
    
    add_person_values = (data['firstName'],data['lastName'],data['email'],data['phone'])
    check_person_values = (data['email'])
    
    try:
		c.execute(check_person,check_person_values)

		if c.rowcount != 0:
			print("Status: 202 Invalid email\n")			
			
		else:
			c.execute(add_person,add_person_values)
			person_pk = c.lastrowid
			
			add_person2 = ("INSERT INTO VMS_persons(person_pk,password,phone_type) VALUES(%s,%s,%s)")
			add_person_values2 = (person_pk, data['password'],data['phone_type'])
			
			c.execute(add_person2,add_person_values2)						
			conn.commit()			
			print("Status: 200 OK\n")
        
    except Exception as e:
        print("Status: 430 Invalid Request\n")
        
else:
    print("Status: 460 Invalid Request\n")