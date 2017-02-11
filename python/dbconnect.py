import MySQLdb

def connection():
    conn = MySQLdb.connect(user = "root",passwd = "2511",db = "cwatest")
    c = conn.cursor()
    return c, conn
