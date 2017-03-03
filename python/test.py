#!/usr/bin/python2.7
import cgitb; cgitb.enable()
import MySQLdb
import cgi
import sys
import helper

try: import simplejson as json
except ImportError: import json

print "Content-type: application/json\n"
print ""
form = cgi.FieldStorage()

data = { 'email':"DONGYAO", 'password':"PASSWORD"}

print(json.JSONEncoder().encode(data))

