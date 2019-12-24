import sys
import mysql.connector
import view as viewer #import view

class Controller:
    def __init__(self, mydb):
        cursor = mydb.cursor()
        # fixing utf problem
        cursor.execute("SET NAMES utf8mb4")
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")

        while (True): 
            choice = viewer.homeView() # call main menu
            if (choice == 1):
                print('member')
            elif (choice == 2):
                self.bookHandler(cursor)
            elif (choice == 3):
                self.loanHandler(cursor)
            elif (choice == 4):
                print('exit')
                sys.exit()
            else:
                viewer.invalidInput()
            mydb.commit() # commit changes in database

    def loanHandler(self, cursor):
        choice = viewer.loanView()
        if (choice == 1):
            print('user want to add new loan detail')
        elif (choice == 2):
            print('user want to delte new loan detail')
        else:
            viewer.invalidInput()

    def bookHandler(self, cursor):
        choice = viewer.bookView()
        if (choice == 1):
            book = viewer.addBook() # book as tuple
            self.insertToDatabase(cursor, "book", book)
        elif (choice == 2):
            print('edit')
        elif (choice == 3):
            print('delete')
        else:
            viewer.invalidInput()

    """
    @op = opration code (book | member | loan)
    @item = item that need to be add in database (tuples)
    """
    def insertToDatabase(self, cursor, op ,item):
        if (op == 'book'): # add book
            print('save book to database')
            print(item)
            mySql_insert_query = 'INSERT IGNORE INTO Book (name, author, edition) VALUES (%s, %s, %s)'
            # note: book = (name, author, edit, bType) 
            val = (item[0], item[1], item[2])
            cursor.execute(mySql_insert_query, val)
            
            ## add book type here
            bookid = cursor.lastrowid # get the id of just added book
            mySql_insert_query = 'INSERT IGNORE INTO BookType (type, bookId) VALUES (%s, %s)'
            val = (item[3], bookid)
            cursor.execute(mySql_insert_query, val)

        elif( op == 'member'):
            print('save member to database')
            # do some sql here
        else:
            print('save loan details')
            # do some sql here

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


controller = Controller(mydb) #create a Controller
