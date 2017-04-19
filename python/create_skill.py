#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
import re
from helper import connectDb, sendJson

# Not currently in use
# Admin side file to create common skills that each job can have
# Inputs - skillName,skillDiscription
# Outputs - {Sucess:True},400

form = cgi.FieldStorage()
# Fake data:
data = {'skill_name':form.getvalue('skillName'),'skill_description':form.getvalue('skillDiscription')}
#data = {'skill_name':'helium','skill_description':'use a helium tank'}

#Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 500 Database Connection Error\n")
	print e
	exit(1)

# Check if the input json value is valid
if not(data["skill_name"] and data["skill_description"]):
	print("Status: 400 Request value is empty\n")
	exit(1)

#SQL
checkSkillSQL = "SELECT skill_id FROM VMS_skills WHERE skill_name = %s"
insertSkillSQL = "INSERT INTO VMS_skills(skill_name,skill_description) values(%s,%s);"

# Run search_skill.py before create skill, therefore no need to check duplication anymore
# Check duplication: if the skill_name already exist in VMS_skills and find the corresponding skill_id
try:
	cursor.execute(checkSkillSQL,[data['skill_name']])
	if cursor.rowcount > 0:
		print("Status: 400 skill_name already exist in VMS_skills\n")
		print e
		exit(1)
except Exception as e:
	print("Status: 400 Invalid MySQL Request(check skill_id duplication\n")
	print e
	exit(1)

# Insert the skill_name and skill_description into vms_skill
try:
	cursor.execute(insertSkillSQL,[data['skill_name'],data['skill_description']])
	connection.commit()
except Exception as e:
	print("Status: Invalid MySQL Request(insert value into vms_voluteer_availability)\n")
	print e
	exit(1)

print("Content-type: application/json")
print("Status: 200 Event created\n")
success = {'Success':True}
print sendJson(success)
