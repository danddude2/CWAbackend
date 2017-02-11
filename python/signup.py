#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
import bcrypt
#Database insertion for signing up

try: import simplejson as json
except ImportError: import json

print "Content-type: application/json\n"
print ""
form = cgi.FieldStorage()

db = "cwatest2"
data = { 'firstName':form['firstName'].value, 'lastName':form['lastName'].value, 'email':form['email'].value,'phone':form['phone'].value, 'password':form['password'].value}

hashed = bcrypt.hashpw(str(attempted_password),bcrypt.gensalt())

conn = MySQLdb.connect(user = "root",passwd = "2511",db) # change the name of this
c = conn.cursor()

try:
	

try:
	# create on general instance of the job 
	check_person = ("SELECT username FROM VMS_persons WHERE username=%s UNION SELECT email FROM VMS_persons WHERE email=%s")
	
	check_vaules = (
	
		
	add_person = ("INSERT INTO VMS_events "
				 "(event_name,event_description) "
				 "VALUES (%s,%s)")
	add_values = (event_name,event_description)	
	
	c.execute(add_person, values)
	conn.commit()
	
	c.close()
	conn.close()
	        
except MySQLdb.Error as err:
        print(err)

	c.execute("SELECT username FROM VMS_persons WHERE username=%s UNION SELECT email FROM VMS_persons WHERE email=%s",[attempted_username,attempted_email])
	if c.rowcount == 0:
		c.execute("INSERT INTO VMS_persons(username,password,email,first_name,last_name) VALUES(%s,%s,%s,%s,%s)",[attempted_username,hashed,attempted_email,attempted_firstname,attempted_lastname])
		conn.commit()
		return redirect(url_for('dashboardpage'))
	else:
		response = 'username or email is already taken'
		conn.rollback()
		return render_template("signup.html",error=response)
except:
	response ="execute failed"
	conn.rollback()
	
return render_template("signup.html",error=response)

print(json.JSONEncoder().encode(data))
