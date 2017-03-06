#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
from helper import connectDb, sendJson
import cgitb; cgitb.enable()
import datetime

form = cgi.FieldStorage()
#data = {'personId': '3'}
data = {'personId':form.getvalue("personId")}
available_times = []
booked_times =[]

# Connect to database
try:
    cursor, connection = connectDb()
except Exception as e:
    print("Status: 400 Database Connection Error\n")
    print e
    exit(1)

getAvailableTimesSQL = "SELECT free_time_start FROM VMS_volunteer_availability WHERE person_pk = %s and job_id is NULL"
getBookedTimesSQL = "SELECT free_time_start FROM VMS_volunteer_availability WHERE person_pk = %s and job_id is not NULL"

# Get information from database
try:
    cursor.execute(getAvailableTimesSQL,[data['personId']])
    avail = cursor.fetchall()
    for times in avail:
        (t,) = times
        t = t.strftime('%Y-%m-%d %H:%M:%S')
        available_times.append(t)
except Exception as e:
    print("Status: 400 Invalid SQL\n")
    print e
    exit(1)

try:
    cursor.execute(getBookedTimesSQL,[data['personId']])
    booked = cursor.fetchall()
    for times in booked:
        (b,) = times
        b = b.strftime('%Y-%m-%d %H:%M:%S')
        booked_times.append(b)
except Exception as e:
    print("Status: 400 Invalid SQL\n")
    print e
    exit(1)
try:
    out_data = {"availableTimes":available_times,"bookedTimes":booked_times}
    print "Content-type: application/json"
    print("Status: 200 OK\n")
    print ""
    print sendJson(out_data)
except Exception as e:
        print("Status: 400 Cannot Get Times\n")
        print e
        exit(1)
