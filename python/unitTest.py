#!/usr/bin/python2.7
import cgi
import cgitb; cgitb.enable()
import unittest
import helper

class TestHelperMethods(unittest.TestCase):
    def test_sendJson(self):
        name = {'lastName':'Ever','firstName':'Greatest'}
        admin = {'admin':True}
        self.assertEqual(helper.sendJson(name,admin),'{"admin": true, "lastName": "Ever", "firstName": "Greatest"}')

    def test_sendEmpty(self):
        none = {}
        self.assertEqual(helper.sendJson(none),'{}')

if __name__ == '__main__':
    print"Status: 200 OK"
    print"Content-Type: application/json"
    print""
    print unittest.main()
