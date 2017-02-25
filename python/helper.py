import MySQLdb
import hashlib
import uuid
try: import simplejson as json
except ImportError: import json

def connectDb():
    connection = MySQLdb.connect("localhost","cwajazz9_vms","radio#492*","cwajazz9_vms")
    cursor = connection.cursor()
    return cursor, connection

def sendJson(*json_objects):
    data = {}
    for items in json_objects:
        data.update(items)
    return json.JSONEncoder().encode(data)

def encrypt(password):
    salt = uuid.uuid4().hex
    hashed = hashlib.sha512(salt+password).hexdigest()
    return hashed, salt
