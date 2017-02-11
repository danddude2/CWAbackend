import MySQLdb
import getpass



conn = MySQLdb.connect(user = "root",passwd = "2511",db = "cwatest2")
c = conn.cursor()

event_name = getpass.getpass("Input event name:")
event_description = getpass.getpass("Input event description:")


try:
	# create on general instance of the job 
	add_event = ("INSERT INTO VMS_events "
				 "(event_name,event_description) "
				 "VALUES (%s,%s)")
	values = (event_name,event_description)	
	
	c.execute(add_event, values)
	conn.commit()
	
	c.close()
	conn.close()
	        
except MySQLdb.Error as err:
        print(err)
