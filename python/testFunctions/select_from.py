#Spills all select results for a specific table

import MySQLdb
import getpass

#switch = input("SELECT * from:\n1.person\n2.VMS_persons\n3.VMS_volunteer_skills\n4.VMS_volunteer_available_time_nodes.VMS_job_types\n4.VMS_skills\n5.VMS_job_assignments\n6.VMS_job_instances\n7.VMS_message_details\n8.VMS_message_types\n9.VMS_job_skills\n10.VMS_volunteer_skills\n11.VMS_volunteer_available_time_nodes\n")
thing = str(getpass.getpass("Input tables:"))

'''
if(switch == 1):
    table = 'person'
'''
cnx = MySQLdb.connect(user='root', passwd =password , db = 'cwatest')
cursor = cnx.cursor()

try:
        cursor.execute("SELECT * FROM %s;"% thing)
        tables = cursor.fetchall()

except MySQLdb.Error as err:
        print(err)
else:
        for row in tables:
                print"".join(row)
