import sys
import mysql.connector
import view as viewer #import view
from datetime import datetime
import time

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
                self.memberHandler(cursor)
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
            print('Please enter following informations to make a new loan (borrow book)')
            personNum = viewer.getPersonNum()
            members = self.getMemberId(cursor, personNum) # get member id by member.personNumber
            if not self.isEmpty('member' ,members): # check is member exist
                memberId = members[0]
                bookKey = viewer.getBookID()
                # book = (bookName, bookEdition)
                books = self.getBookId(cursor, bookKey[0], bookKey[1])
                if not self.isEmpty('book', books): # check if book exist
                    bookId = books[0]
                    # check if the loanDetails is exist
                    if self.stockHandler(cursor, 'borrow' ,booksId):
                         #get the first tuple
                        current = time.time()  # current time in unix time
                        threeWeek = 1814400 # three time in unix time
                        expired = current + threeWeek 
                        expired = datetime.fromtimestamp(int(expired))
                        current = datetime.fromtimestamp(int(current))
                        # now insert loan detail
                        val = (current, expired, bookId[0], memberId[0])
                        self.insertToDatabase(cursor, 'loan', val)
            else:
                pass    
        elif (choice == 2):
            print('Please enter following information to return the book')
            personNum = viewer.getPersonNum()
            members = self.getMemberId(cursor, personNum) # get member id by member.personNumber
            if not self.isEmpty('member' ,members): # check is member exist
                memberId = members[0]
                bookKey = viewer.getBookID()
                books = self.getBookId(cursor, bookKey[0], bookKey[1])
                if not self.isEmpty('book', books): # check if book exist
                    bookId = books[0] #get the first tuple
                    mySql_select_query = "SELECT * FROM `LoanDetails` WHERE book_id = %s AND member_id = %s"
                    cursor.execute(mySql_select_query, (bookId[0], memberId[0]))
                    records = cursor.fetchall()
                    if not self.isEmpty('loan', records):
                        self.stockHandler(cursor, 'return', bookId[0])
                        self.deleteFromDatabase(cursor, 'loan', (bookId[0], memberId[0]))                    
        else:
            viewer.invalidInput()

    def stockHandler(self, cursor, op, bookId):
        mySql_select_query = "select amount from bookStock where book_id = %s"
        cursor.execute(mySql_select_query, (bookId, ))
        records = cursor.fetchone()
        stock = int(records[0])
        if stock == 0: ## no book left in stock
            return False
            print('[+] Error: OUT OF STOCK\nThis book is not in the library at the moment')
        else: 
            if (op == 'borrow'):
                # borrow book -> decrease the stock
                mySql_update_query = "UPDATE Stock SET amount = amount - 1 where Stock.book_id = %s;"
                cursor.execute(mySql_update_query, (bookId[0], ))
            else:
                # return book -> increase the stock
                mySql_update_query = "UPDATE Stock SET amount = amount + 1 where Stock.book_id = %s;"
                cursor.execute(mySql_update_query, (bookId, )) 
            return True

    def isEmpty(self, op, item):
        output = ''
        if (len(item) == 0): # the tuple is empty
            if (op == 'member'):
                print('[+] ERROR: Member is not exist in the database')
            elif (op == 'book'):
                print('[+] ERROR: Book is not exist in the database')
            elif (op == 'loan'):
                print('[+] ERROR: there is NO data about this specific loan in the database')
            return True
        else:
            return False
        
    def getBookId(self, cursor, name, edition):
        mySql_select_query = "SELECT bkID FROM `Book` WHERE name = %s AND edition = %s"
        cursor.execute(mySql_select_query, (name, edition))
        records = cursor.fetchall()
        return records

    def getMemberId(self, cursor, personNum):
        mySql_select_query = "SELECT memID FROM `Member` WHERE personalNum = '%s' "
        cursor.execute(mySql_select_query, (personNum,))
        records = cursor.fetchall()
        return records

    def bookHandler(self, cursor):
        choice = viewer.bookView()
        if (choice == 1):
            book = viewer.addBook() # book as tuple
            self.insertToDatabase(cursor, "book", book)
        elif (choice == 2):
            print('delete')
        elif (choice == 3):
            print('edit')
        else:
            viewer.invalidInput()
    
    def memberHandler(self, cursor):
        choice = viewer.memberView()
        if(choice == 1):
            member = viewer.addMember()
            self.insertToDatabase(cursor, "member", member)
        elif(choice == 2):
            personNum = viewer.getPersonNum()
            self.deleteFromDatabase(cursor, 'member', personNum)
        elif(choice == 3):
            print('edit mem')
        else: 
            viewer.invalidInput()

    """
    @op = opration code (book | member | loan)
    @item = item that need to be add in database (tuples)
    """
    def insertToDatabase(self, cursor, op ,item):
        if( op == 'member'):
            # note: member = (firstName, lastName, gender, address, personalNumn)
            mySql_insert_query = "INSERT IGNORE INTO `Member` (firstName, lastName, gender, address, personalNum) VALUES (%s, %s, %s, %s, %s)"
            val = (item[0], item[1], item[2], item[3], int(item[4]))
            cursor.execute(mySql_insert_query, val)
            print('[+] SUCESFUL: The MEMBER has been added into the database')

        elif (op == 'book'): 
            # add book
            # note: book = (name, author, edit, bType) 
            mySql_insert_query = 'INSERT IGNORE INTO Book (name, author, edition, type) VALUES (%s, %s, %s, %s)'
            val = (item[0], item[1], item[2], item[3])
            cursor.execute(mySql_insert_query, val)
            
            ## add stock
            bookid = cursor.lastrowid # get the id of just added book
            mySql_insert_query = 'INSERT IGNORE INTO Stock (amount, book_id) VALUES (%s, %s)'
            val = (item[4], bookid)
            cursor.execute(mySql_insert_query, val)
            print('[+] SUCCESSFUL: The stock has been added into the database')

        else:
            mySql_insert_query = 'INSERT IGNORE INTO `LoanDetails` (date, expireDate, book_id, member_id) VALUES (%s, %s, %s, %s)'
            cursor.execute(mySql_insert_query, (item[0], item[1], item[2], item[3]))
            print('[+] SUCCESSFUL: The LOAN detail has been added into the database')

    """
    @op = opration code (book | member | loan)
    @keyTodelete = The key which will be use for searching for the object
    """
    def deleteFromDatabase(self, cursor, op, keyTodelete ):
        if(op == 'member'):
            # try to select first, if it do not exist then prompt an SUCCESSFUL. if exist then -> delete it
            members = self.getMemberId(cursor, keyTodelete) # get member id by member.personNumber
            if not self.isEmpty('member' ,members): # check is member exist
                memberId = members[0]
                mySql_delete_query = "delete from `Member` where personalNum = '%s' " 
                cursor.execute(mySql_delete_query, (keyTodelete,)) 
                print('[+] SUCCESSFUL: The member has been deleted from database')
                
        elif(op == 'book'):
            print('delete book')
        else:
            mySql_delete_query = "delete from `LoanDetails` WHERE book_id = %s AND member_id = %s"
            cursor.execute(mySql_delete_query, (keyTodelete[0], keyTodelete[1])) # memTodelete[0] = bookId [1] = memberId
            print('[+] SUCCESSFUL: The loan detail has been deleted from database')

            
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
