import mysql.connector
from config import config

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

cursor.execute('SELECT ticketid, fromid FROM transactions')

for (ticketid) in cursor:
  print(f"Id: {ticketid}")

cursor.close()

cnx.close()