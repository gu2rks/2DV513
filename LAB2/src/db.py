import sys
import mysql.connector
import json
import threading
import time
from datetime import datetime


SUBREDDIT = "Subreddit"
COMMENT = "Comment"
LINK = "Link"


def connect(): # connect to mysql database
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user='root',
            passwd=str(sys.argv[1]),
            db=str(sys.argv[2])
        )
    except Exception as e:
        print(e)
        sys.exit("Can't connect to database")
    return mydb


def saveToDatabase(cursor, table, item): # insert data in mysql table by table
    if table == SUBREDDIT: # insert in subreddit table
        mySql_insert_query = 'INSERT IGNORE INTO Subreddit (id, name) VALUES (%s, %s) ' 
        val = (item["subreddit_id"], item["subreddit"])
        cursor.execute(mySql_insert_query, val)
    elif table == LINK: # insert to Link table
        mySql_insert_query = 'INSERT IGNORE INTO Link (id, subreddit_id) VALUES (%s, %s)'
        val = (item["link_id"], item["subreddit_id"])
        cursor.execute(mySql_insert_query, val)
    else:   # insert to Comment table
        mySql_insert_query = 'INSERT IGNORE INTO Comment (id, name, author, createdUTC, parentID, body, score, link_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        val = (item["id"], item["name"], item["author"], datetime.fromtimestamp(int(item["created_utc"])),
               item["parent_id"], str(item["body"]), item["score"], item["link_id"])
        cursor.execute(mySql_insert_query, val)

# def thread_function(mydb, item):
#     cursor = mydb.cursor()
#     j = json.loads(item)
#     saveToDatabase(cursor, SUBREDDIT, j)
#     saveToDatabase(cursor, COMMENT, j)
#     saveToDatabase(cursor, LINK, j)
#     mydb.commit()

if len(sys.argv) - 1 <= 2:
    print('## ERROR!! python3 db.py [password] [NameDatabase] [FileAbsolutePath]')
    sys.exit()
else:
    count = 0
    mydb = connect()
    # threads = list()
    cursor = mydb.cursor()
    # fixing utf problem
    cursor.execute('SET NAMES utf8mb4')
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
    start_time = time.time()
    try:
        with open(sys.argv[3], 'r') as data:
            for line in data:
                j = json.loads(line) # convert to item to json
                saveToDatabase(cursor, SUBREDDIT, j)
                saveToDatabase(cursor, LINK, j)
                saveToDatabase(cursor, COMMENT, j)
                count += 1
                # print('added %s in the database'  %count)
                mydb.commit() # commit changes in databes
        
                # Threadding
                # x = threading.Thread(target=thread_function, args=(mydb,line))
                # threads.append(x)
                # x.start()
                # x.join()
        print("--- %s seconds ---" % (time.time() - start_time))
    except FileNotFoundError:
        print('## ERROR: FILE NOT FOUND, wrong path')
