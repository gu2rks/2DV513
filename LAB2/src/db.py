import sys
import mysql.connector
import json
# import threading
import time


SUBREDDIT = "Subreddit"
COMMENT = "Comment"
LINK = "Link"
def connect ():
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

def readFile ():
    fileHandler = open (sys.argv[3], "r")
    data = fileHandler.readlines()
    fileHandler.close()
    return  data

def saveToDatabase (cursor, table, item):
    if table == SUBREDDIT:
        mySql_insert_query = 'INSERT INTO Subreddit (id, name) VALUES (%s, %s) '
        val = (item["subreddit_id"], item["subreddit"])
        cursor.execute(mySql_insert_query, val)
    elif table == LINK:
        mySql_insert_query = 'INSERT INTO Link (id) VALUES (%s)'
        val = (item["link_id"],)
        cursor.execute(mySql_insert_query, val)
    else:
        mySql_insert_query = 'INSERT INTO Comment (id, name, author, createdUTC, parentID, body, score) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        val = (item["id"], item["name"], item["author"], item["created_utc"], item["parent_id"], item["body"], item["score"] )
        cursor.execute(mySql_insert_query, val)

# def thread_function(mydb, item):
#     cursor = mydb.cursor()
#     j = json.loads(item)
#     saveToDatabase(cursor, SUBREDDIT, j)
#     saveToDatabase(cursor, COMMENT, j)
#     saveToDatabase(cursor, LINK, j)
#     mydb.commit()


if len(sys.argv) - 1 <= 2:
    print('ERROR!! python3 db.py [password] [NameDatabase] [FileAbsolutePath]')
else:
    mydb = connect()
    data = readFile()
    # threads = list()
    start_time = time.time()
    for item in data: # insert data to subreddit table

        ## Threadding
        # x = threading.Thread(target=thread_function, args=(mydb,item))
        # threads.append(x)
        # x.start()
        # x.join()
        cursor = mydb.cursor()
        j = json.loads(item)
        saveToDatabase(cursor, SUBREDDIT, j)
        saveToDatabase(cursor, COMMENT, j)
        saveToDatabase(cursor, LINK, j)
        mydb.commit()
    print("--- %s seconds ---" % (time.time() - start_time))