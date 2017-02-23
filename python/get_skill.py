#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
import re
try: import simplejson as json
except ImportError: import json



#form = cgi.FieldStorage()
# Fake data:
data = {'skill_name':'dancer'}




# Connect to database
try:
    conn = MySQLdb.connect(user='root', passwd = '2511', db = 'cwajazz9_vms')
    c = conn.cursor()
except Exception as e:
    print("Status: Database connection initiation error")
    exit(1)



# Check if the input jason value is valid
if not(data["skill_name"]):
	print("Status: Some JSON value is empty\n")
	exit(1)



# Check if the skill_name already exist in VMS_skills and find the corresponding skill_id
try:
	c.execute("select skill_id from vms_skills where skill_name = %s",[data['skill_name']])
	if c.rowcount == 0:
		print("Status: skill_name does not exist in VMS_skills")
		exit(1)
except Exception as e:
	print("Status: Invalid MySQL Request(check skill_id duplication")
	exit(1)



# Return the skill_id, skill_name, skill_description created
try:
	c.execute("select skill_id,skill_name,skill_description from vms_skills where skill_name = %s",[data['skill_name']])
	return_data = c.fetchall()
except Exception as e:
	print("Status: Invalid MySQL Request(check returned skill_id")
	exit(1)



# Inset data into json format
out_data = {}
for i in range(len(return_data)):
	out_data.update({"skill_id"+str(i):int(return_data[i][0])})
	out_data.update({"skill_name"+str(i):return_data[i][1]})
	out_data.update({"skill_description"+str(i):return_data[i][2]})


print out_data








