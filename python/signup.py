#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi

form = cgi.FieldStorage()
try:
    conn = MySQLdb.connect("localhost", "cwajazz9_vms", "radio#492*", "cwajazz9_vms")
    c = conn.cursor()
except Exception as e:
    print("Status: 500 Server Error\n")
    exit(1)
if form.has_key("firstName") and form.has_key("lastName") and form.has_key("email") and form.has_key("phone") and form.has_key("password"):
    firstName = form.getvalue("firstName")
    lastName = form.getvalue("lastName")
    email = form.getvalue("email")
    phone = form.getvalue("phone")
    password = form.getvalue("password")
    #sql = ("INSERT INTO VMS_persons(firstName,lastName,email,phone,password) VALUES(%s,%s,%s,%s,%s);")
    #values = (firstName,lastName,email,phone,password)
    try:
        c.execute("INSERT INTO VMS_persons(first_name,last_name,email,phone,password) VALUES(%s,%s,%s,%s,%s)",[firstName,lastName,email,phone,password])
        conn.commit()
        print("Status: 200 OK\n")
    except Exception as e:
        print("Status: 430 Invalid Request\n")
else:
    print("Status: 460 Invalid Request\n")
