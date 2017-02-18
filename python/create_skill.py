#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
import re
try: import simplejson as json
except ImportError: import json


#form = cgi.FieldStorage()
data = {'skill_name':'dancer','skill_description':'dance twice'}


# Connect to database
try:
    conn = MySQLdb.connect(user='root', passwd = '2511', db = 'cwatest2')
    c = conn.cursor()
except Exception as e:
    print("Status: Database connection initiation error")
    exit(1)


# Check if the input jason value is valid
if not(data["skill_name"] and data["skill_description"]):
	print("Status: Some JSON value is empty\n")
	exit(1)

'''
# Run search_skill.py before create skill, therefore no need to check duplication anymore
# Check duplication: if the skill_name already exist in VMS_skills and find the corresponding skill_id
try:
	c.execute("select skill_id from vms_skills where skill_name = %s",[data['skill_name']])
	if c.rowcount > 0:
		print("Status: skill_name already exist in VMS_skills")
		exit(1)
except Exception as e:
	print("Status: Invalid MySQL Request(check skill_id duplication")
	exit(1)
'''

# Insert the skill_name and skill_description into vms_skill
try:
	c.execute("insert into vms_skills(skill_name,skill_description)values(%s,%s);",[data['skill_name'],data['skill_description']])
	conn.commit()
except Exception as e:
	print("Status: Invalid MySQL Request(insert value into vms_voluteer_availability)\n")
	exit(1)


# Return the skill_id created
try:
	c.execute("select skill_id from vms_skills where skill_name = %s",[data['skill_name']])
	return_id = str(c.fetchall()[0][0])
except Exception as e:
	print("Status: Invalid MySQL Request(check returned skill_id")
	exit(1)


print 'Status: Success ! '+data['skill_name']+' skill_id : '+return_id




