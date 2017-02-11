#Example job creation
import MySQLdb
import getpass
from dbconnect import connection


c, conn = connection()

job_type_id = int(float(getpass.getpass("Input  job type id:")))
#job_time = getpass.getpass("Input job time:")
location = getpass.getpass("Input location:")
job_description = getpass.getpass("Input job description:")
volunteers_needed = int(float(getpass.getpass("Input # of volunteers:")))


try:
	# create on general instance of the job 
	c.execute("INSERT INTO VMS_jobs(job_type_id,location,job_description,volunteers_needed) VALUES(%d,%s,%s,%d)" % \
		(job_type_id,location,job_description,volunteers_needed))
		
	
	c.execute("SELECT job_id from VMS_job_instances WHERE location=%s AND job_description=%s",  \
		[location,job_description])		
	for fetch_id in c:
                    jobid = fetch_id
    #cursor.lastrowid             
                    
	
	print jobid
	# create a specific assingment for each volunteer needed (no person assigned 	
	for x in range(0,volunteers_needed):
		c.execute("INSERT INTO VMS_job_assignments(person_id,job_id) VALUES(-1,%s)" % jobid)
	
		
        
except MySQLdb.Error as err:
        print(err)

