import sys
import mysql.connector
import view as viewer #import view

class Controller:
    mydb = None #gobal object for database

    def __init__(self):
        try: # connecto the database
            mydb = mysql.connector.connect(
                host="localhost",
                user='root',
                passwd=str(sys.argv[1]),
                db='Library'
            )
        except Exception as e:
            print(e)
            sys.exit("Can't connect to database")

        choice = viewer.home() # call main menu
        print(choice)

#validate user input
if len(sys.argv) < 1:
    print('## ERROR!! python3 library.py [password]')
    sys.exit()

controller = Controller() #create a Controller object
