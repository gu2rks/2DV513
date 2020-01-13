import sys
import mysql.connector
import view as viewer  # import view
import databaseManager as dbManager # import database manager
import datetime
# from datetime import datetime
import time


class Controller:    
    def __init__(self, mydb):
        cursor = mydb.cursor()
        # fixing utf problem
        cursor.execute("SET NAMES utf8mb4")
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")

        while (True):
            choice = viewer.homeView()  # call main menu
            if (choice == 1):
                self.memberHandler(cursor)
            elif (choice == 2):
                self.bookHandler(cursor)
            elif (choice == 3):
                self.loanHandler(cursor)
            elif (choice == 4):
                dbManager.bestBooks(cursor)
            elif (choice == 5):
                dbManager.bestReader(cursor)
            elif (choice == 6):
                print('Exit the program')
                sys.exit()
            else:
                viewer.invalidInput()
            mydb.commit()  # commit changes in database

    def loanHandler(self, cursor):
        choice = viewer.loanView()
        if (choice == 1):
            print('Please enter following informations to make a new loan (borrow book)')
            personNum = viewer.getPersonNum()
            # get member id by member.personNumber
            members = dbManager.getMemberId(cursor, personNum)
            if not dbManager.isEmpty(MEMBER, members):  # check is member exist
                memberId = members[0]
                bookKey = viewer.getBookID()
                # book = (bookName, bookEdition)
                books = dbManager.getBookId(cursor, bookKey[0], bookKey[1])
                if not dbManager.isEmpty(BOOK, books):  # check if book exist
                    bookId = books[0]
                    # check if the loanDetails is exist
                    if dbManager.stockHandler(cursor, BORROW, bookId[0]):
                         # get the first tuple
                        current = time.time()  # current time in unix time
                        threeWeek = 1814400  # three time in unix time
                        expired = current + threeWeek
                        expired = datetime.date.fromtimestamp(int(expired))
                        current = datetime.date.fromtimestamp(int(current))
                        # now insert loan detail
                        val = (current, expired, bookId[0], memberId[0])
                        dbManager.insertRecord(cursor, LOAN, val)
            else:
                pass
        elif (choice == 2):
            print('Please enter following information to return the book')
            personNum = viewer.getPersonNum()
            # get member id by member.personNumber
            members = dbManager.getMemberId(cursor, personNum)
            if not dbManager.isEmpty( MEMBER, members):  # check is member exist
                memberId = members[0]
                bookKey = viewer.getBookID()
                books = dbManager.getBookId(cursor, bookKey[0], bookKey[1])
                if not dbManager.isEmpty(BOOK , books):  # check if book exist
                    bookId = books[0]  # get the first tuple
                    mySql_select_query = "SELECT * FROM `LoanDetails` WHERE book_id = %s AND member_id = %s"
                    cursor.execute(mySql_select_query,
                                   (bookId[0], memberId[0]))
                    records = cursor.fetchall()
                    if not dbManager.isEmpty(LOAN, records):
                        dbManager.stockHandler(cursor, RETURNBOOK, bookId[0])
                        dbManager.deleteRecord(
                            cursor, LOAN, (bookId[0], memberId[0]))
        elif (choice == 3):
            exprie = viewer.exprie()
            date = datetime.date(int(exprie[0]), int(exprie[1]), int(exprie[2]))
            dbManager.getMemberbyExpriedDay(cursor,date)
        else:
            viewer.invalidInput()

    def bookHandler(self, cursor):
        choice = viewer.bookView()
        if (choice == 1):
            book = viewer.addBook()  # book as tuple
            dbManager.insertRecord(cursor, BOOK, book)
        else:
            book = viewer.getBookID()
            records = dbManager.getBookId(cursor, book[0], book[1])
            if not dbManager.isEmpty(BOOK, records): 
                if (choice == 2):
                        bookId = records[0]
                        dbManager.deleteRecord(cursor, BOOK, bookId[0])
                elif (choice == 3):
                        bookId = records[0]
                        dbManager.updateRecord(cursor, BOOK, bookId[0])            
            else:
                viewer.invalidInput()

    def memberHandler(self, cursor):
        choice = viewer.memberView()
        if(choice == 1):
            member = viewer.addMember()
            dbManager.insertRecord(cursor, MEMBER, member)
        else:
            personNum = viewer.getPersonNum()
            records = dbManager.getMemberId(cursor, personNum)
            # check if member exist in database
            if (not dbManager.isEmpty(MEMBER,records)):
                memberId = records[0]
                if(choice == 2):
                    dbManager.deleteRecord(cursor, MEMBER, memberId[0])
                elif(choice == 3):
                    dbManager.updateRecord(cursor, MEMBER, memberId[0])
                elif (choice == 4):
                    # check if member has borrow anybook
                    mySql_select_query = "SELECT * FROM `LoanDetails` WHERE member_id = %s"
                    cursor.execute(mySql_select_query, (memberId[0],))
                    records = cursor.fetchall()
                    if not dbManager.isEmpty(LOAN, records):
                        dbManager.getBorrowedBookByMember(cursor, personNum)
            else:
                viewer.invalidInput()

""" 
MAIN
"""
# validate user input
if len(sys.argv) < 1:
    print('[+] ERROR: USECASE python3 library.py [password]')
    sys.exit()

try:  # connecto the database
    mydb = mysql.connector.connect(
        host="localhost",
        user='root',
        passwd=str(sys.argv[1]),
        db='Library'
    )
except Exception as e:
    print(e)
    sys.exit("Can't connect to database")


MEMBER = 'member'
BOOK = 'book'
LOAN = 'loan'
BORROW = 'borrow'
RETURNBOOK = 'return'
controller = Controller(mydb)  # create a Controller
