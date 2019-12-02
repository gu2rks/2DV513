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

null = None
true = True
false = False

data = [{"parent_id":"t3_5yba3","created_utc":"1192450635","ups":1,"controversiality":0,"distinguished":null,"subreddit_id":"t5_6","id":"c0299an","downs":0,"archived":true,"link_id":"t3_5yba3","score":1,"author":"bostich","score_hidden":false,"body":"test","gilded":0,"author_flair_text":null,"subreddit":"reddit.com","edited":false,"author_flair_css_class":null,"name":"t1_c0299an","retrieved_on":1427426409},
{"author_flair_text":null,"gilded":0,"score_hidden":false,"body":"[deleted]","score":1,"link_id":"t3_5yba3","author":"[deleted]","name":"t1_c0299aq","retrieved_on":1427426409,"author_flair_css_class":null,"subreddit":"reddit.com","edited":false,"ups":1,"controversiality":0,"created_utc":"1192450646","parent_id":"t3_5yba3","archived":true,"downs":0,"subreddit_id":"t5_6","id":"c0299aq","distinguished":null},
{"edited":false,"subreddit":"reddit.com","author_flair_css_class":null,"name":"t1_c0299ar","retrieved_on":1427426409,"author":"gigaquack","link_id":"t3_5yba3","score":3,"body":"Oh, I see. Fancy schmancy \"submitting....\"","score_hidden":false,"author_flair_text":null,"gilded":0,"distinguished":null,"subreddit_id":"t5_6","id":"c0299ar","downs":0,"archived":true,"created_utc":"1192450646","parent_id":"t1_c0299ah","controversiality":0,"ups":3}
]

if len(sys.argv) - 1 == 0:
    print ('ERROR!! python3 db.py [password]')
else:
    connect()

