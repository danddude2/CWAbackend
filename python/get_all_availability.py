#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
from helper import connectDb, sendJson, time_node_to_datetime
import datetime
from datetime import date
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
#data = {'eventId':'1'}
data = {'eventId':form.getvalue("eventId")}
out_data ={}
# Connect to database
try:
    cursor, connection = connectDb()
except Exception as e:
    print("Status: 400 Database Connection Error\n")
    print e
    exit(1)

getVolunteers = "SELECT DISTINCT person_pk FROM VMS_volunteer_availability WHERE event_id = %s"
getAvailableTimesSQL = "SELECT free_time_start FROM VMS_volunteer_availability WHERE person_pk = %s and event_id = %s"
getDesiredHoursSQL = "SELECT desired_hours FROM VMS_persons WHERE person_pk = %s"
getJobsSQL = "SELECT job_id FROM VMS_jobs WHERE event_id = %s and person_pk = %s"
getEventsSQL = "SELECT * from VMS_jobs WHERE person_pk = %s AND event_id = %s"

volunteer_array = []
try:
    cursor.execute(getVolunteers,[data['eventId']])
    avail = cursor.fetchall()
    for pks in avail:
        (ids,) = pks
        volunteer_array.append(str(ids))
except Exception as e:
    print("Status: 400 Invalid SQL get volunteers\n")
    print e
    exit(1)

for ids in volunteer_array:
    available_times = []
    # Get information from database
    try:
        cursor.execute(getAvailableTimesSQL,[ids,data['eventId']])
        availTimes = cursor.fetchall()
        for times in availTimes:
            (t,) = times
            t = t.strftime('%Y-%m-%d %H:%M:%S')
            available_times.append(t)
    except Exception as e:
        print("Status: 400 Invalid SQL get available times\n")
        print e
        exit(1)
    try:
        cursor.execute(getDesiredHoursSQL,[ids])
        (desired_hours,) = cursor.fetchone()
    except Exception as e:
        print("Status: 400 Invalid SQL get desidred hours\n")
        print e
        exit(1)
    try:
        cursor.execute(getEventsSQL,[ids,data['eventId']])
        return_data = cursor.fetchall()
    except Exception as e:
        print("Status: 400 Invalid SQL\n")
        print e
        exit(1)
    try:
        job_data = {}
        # Insert data into josn format
        for i in range(len(return_data)):
            job = {}
            job_time_date = str(return_data[i][3])[0:10]
            job_time_start_hour = str(return_data[i][3])[11:16]
            job_time_end_hour = str(return_data[i][4])[11:16]
            job.update({'job_name':return_data[i][7]})
            job.update({'event_id':int(return_data[i][1])})
            job.update({'person_pk':return_data[i][2]})
            job.update({'job_date':job_time_date})
            job.update({'job_time_start':job_time_start_hour})
            job.update({'job_time_end':job_time_end_hour})
            job.update({'location':return_data[i][5]})
            job.update({'job_description':return_data[i][6]})
            job.update({'job_status':return_data[i][8]})
            job_data.update({str(return_data[i][0]):job})

        timeRange = time_node_to_datetime(available_times)
        volunteer_data = {"availableTimes": timeRange,"desiredHours":desired_hours,"jobs":job_data}
        out_data.update({ids:volunteer_data})
    except Exception as e:
           print("Status: 400 Cannot Get Times\n")
           print e
           exit(1)
try:
    print "Content-type: application/json"
    print("Status: 200 OK\n")
    print sendJson(out_data)
except Exception as e:
    print("Status: 400 Cannot Get Times\n")
    print e
    exit(1)
