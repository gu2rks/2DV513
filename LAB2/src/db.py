import sys
import mysql.connector
import json

def connect():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = 'root',
        passwd = str(sys.argv[1])
    )
    print(mydb)

if len(sys.argv) - 1 == 0:
    print ('ERROR!! python3 db.py [password]')
else:
    connect()

