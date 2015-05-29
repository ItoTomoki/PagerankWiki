import mysql.connector
import MySQLdb
connector = MySQLdb.connect(host="localhost", db="twitter", user="root",passwd="", charset="utf8")
cursor = connector.cursor()
sql = u"SELECT * FROM tweets;"
cursor.execute(sql)
result = cursor.fetchall()
print result[0][2]
cursor.close()
connector.close()