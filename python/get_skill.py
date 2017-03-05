#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
import re
from helper import connectDb, sendJson

form = cgi.FieldStorage()
# Fake data:
data = {'skill_id':form.getvalue("skillId")}
#data = {'skill_id' : '2'}
# Connect to database
try:
	cursor, connection = connectDb()
except Exception as e:
	print("Status: 500 Database Connection Error\n")
	print e
	exit(1)

# Check if the input jason value is valid
if not(data["skill_id"]):
	print("Status: Some JSON value is empty\n")
	exit(1)

checkSkill ="SELECT skill_id from VMS_skills WHERE skill_id = %s"
getSkills = "SELECT * from VMS_skills WHERE skill_id= %s"
# Check if the skill_id already exist in VMS_skills and find the corresponding skill_id
try:
	cursor.execute(checkSkill,[data['skill_id']])
	if cursor.rowcount == 0:
		print("Status: skill_id does not exist in VMS_skills")
		exit(1)
except Exception as e:
	print("Status: Invalid MySQL Request(check skill_id duplication")
	exit(1)

# Return the skill_id, skill_id, skill_description created
try:
	cursor.execute(getSkills,[data['skill_id']])
	return_data = cursor.fetchall()
except Exception as e:
	print("Status: Invalid MySQL Request(check returned skill_id")
	exit(1)

# Inset data into json format
out_data = {}
for i in range(len(return_data)):
	out_data.update({"skill_id":int(return_data[i][0])})
	out_data.update({"skill_name":return_data[i][1]})
	out_data.update({"skill_description":return_data[i][2]})
print("Content-type: application/json")
print("Status: 200 OK\n")
print sendJson(out_data)
