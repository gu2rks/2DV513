import sys
import mysql.connector
import json

SUBREDDIT = "Subreddit"
COMMENT = "Comment"
LINK = "Link"

null = None
true = True
false = False

def connect ():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user='root',
            passwd=str(sys.argv[1]),
            db=str(sys.argv[2])
        )
    except Exception as e:
        sys.exit("Can't connect to database")
    return mydb

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


data = [{"parent_id": "t3_5yba3", "created_utc": "1192450635", "ups": 1, "controversiality": 0, "distinguished": null, "subreddit_id": "t5_6", "id": "c0299an", "downs": 0, "archived": true, "link_id": "t3_5yba3", "score": 1, "author": "bostich", "score_hidden": false, "body": "test", "gilded": 0, "author_flair_text": null, "subreddit": "reddit.com", "edited": false, "author_flair_css_class": null, "name": "t1_c0299an", "retrieved_on": 1427426409},
        {"author_flair_text": null, "gilded": 0, "score_hidden": false, "body": "[deleted]", "score": 1, "link_id": "t3_5yba3", "author": "[deleted]", "name": "t1_c0299aq", "retrieved_on": 1427426409, "author_flair_css_class": null,
            "subreddit": "reddit.com", "edited": false, "ups": 1, "controversiality": 0, "created_utc": "1192450646", "parent_id": "t3_5yba3", "archived": true, "downs": 0, "subreddit_id": "t5_6", "id": "c0299aq", "distinguished": null},
        {"edited": false, "subreddit": "reddit.com", "author_flair_css_class": null, "name": "t1_c0299ar", "retrieved_on": 1427426409, "author": "gigaquack", "link_id": "t3_5yba3", "score": 3, "body": "Oh, I see. Fancy schmancy \"submitting....\"",
            "score_hidden": false, "author_flair_text": null, "gilded": 0, "distinguished": null, "subreddit_id": "t5_6", "id": "c0299ar", "downs": 0, "archived": true, "created_utc": "1192450646", "parent_id": "t1_c0299ah", "controversiality": 0, "ups": 3}
        ]

if len(sys.argv) - 1 <= 1:
    print('ERROR!! python3 db.py [password] [NameDatabase]')
else:
    mydb = connect()
    for item in data: # insert data to subreddit table
        cursor = mydb.cursor()
        saveToDatabase(cursor, SUBREDDIT, item)
        saveToDatabase(cursor, COMMENT, item)
        saveToDatabase(cursor, LINK, item)
        mydb.commit()