import sys
import mysql.connector
import view as viewer #import view

class Controller:
    # operation code
    OP1 = 'BOOK'
    OP2 = 'MEMBER'

    def __init__(self, cursor):
        while (True): 
            choice = viewer.homeView() # call main menu
            if (choice == 1):
                print('member')
            elif (choice == 2):
                self.bookHandler(cursor)
            elif (choice == 3):
                print('loan')
            elif (choice == 4):
                print('exit')
                sys.exit()
            else:
                viewer.invalidInput()

    def bookHandler(selft, cursor):
        choice = viewer.bookView()
        if (choice == 1):
            book = viewer.addBook() # book as tuple
            self.saveToDatabase(cursor, OP1, book)
        elif (choice == 2):
            print('edit')
        elif (choice == 3):
            print('delete')
        else:
            viewer.invalidInput()

    """
    @item = book or member
    """
    def insertToDatabase(self, cursor, op ,item):
        if (op == OP1): # add book
            print('save book to database')
        elif( op == OP2):
            print('save member to database')
        else:
            print('save loan details')



"""
MAIN
"""
#validate user input
if len(sys.argv) < 1:
    print('[+] ERROR: USECASE python3 library.py [password]')
    sys.exit()

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

cursor = mydb.cursor()
# fixing utf problem
cursor.execute("SET NAMES utf8mb4")
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection=utf8mb4")

controller = Controller(cursor) #create a Controller object
