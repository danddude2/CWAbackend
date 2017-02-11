import MySQLdb
import getpass

password = getpass.getpass("Input mysql password:")
cnx = MySQLdb.connect(user='root', passwd = password, db = 'cwatest')
cursor = cnx.cursor()
try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
except MySQLdb.Error as err:
        print(err)
else:
        for row in tables:
                print"".join(row)
