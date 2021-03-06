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
        dbManager.setup(cursor)
        try: 
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
                    print('Exit the application')
                    sys.exit()
                else:
                    viewer.invalidInput()
                mydb.commit()  # commit changes in database
        except KeyboardInterrupt as e:
            sys.exit("User pressed ctrl + c to exit the application")

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
            if self.validation(LOAN, exprie):
                date = datetime.date(int(exprie[0]), int(exprie[1]), int(exprie[2]))
                dbManager.getMemberbyExpriedDay(cursor,date)
        elif (choice == 4):
            pass
        else:
            viewer.invalidInput()

    def bookHandler(self, cursor):
        choice = viewer.bookView()
        if (choice == 1):
            book = viewer.addBook()  # book as tuple
            dbManager.insertRecord(cursor, BOOK, book)
        elif (choice == 4):
            pass            
        elif (choice >= 2 and choice <= 3):
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
            personNum = member[4]
            if (self.validation(MEMBER, personNum)):
                dbManager.insertRecord(cursor, MEMBER, member)
        elif (choice == 5):
            pass
        elif (choice >= 2 and choice <= 4):
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

    def validation(self, op, toValidate):
        if (op == MEMBER):
            if (len(toValidate) == 10):
                m = int(toValidate[2:4])
                d = int(toValidate[4:6])
                if (m > 0 and m < 13):
                    if(d > 0 and d < 32):
                        return True
            else:     
                viewer.errorNotexist('personNum')
        elif (op == LOAN):
            try:
                date = datetime.date(int(toValidate[0]), int(toValidate[1]), int(toValidate[2]))
                return True
            except ValueError as e:
                print('[!] Error: ', e)
                return False

""" 
MAIN
"""
# validate user input
if len(sys.argv) < 1:
    print('[+] ERROR: USECASE python3 library.py [password]')
    sys.exit()

intro = '''
88888888ba                          88     I8,        8        ,8I                                        
88      "8b                         88     `8b       d8b       d8'                                        
88      ,8P                         88      "8,     ,8"8,     ,8"                                         
88aaaaaa8P'  ,adPPYba,   ,adPPYba,  88   ,d8 Y8     8P Y8     8P  ,adPPYba,  8b,dPPYba, 88,dPYba,,adPYba, 
88""""""8b, a8"     "8a a8"     "8a 88 ,a8"  `8b   d8' `8b   d8' a8"     "8a 88P'   "Y8 88P'   "88"    "8a
88      `8b 8b       d8 8b       d8 8888[     `8a a8'   `8a a8'  8b       d8 88         88      88      88
88      a8P "8a,   ,a8" "8a,   ,a8" 88`"Yba,   `8a8'     `8a8'   "8a,   ,a8" 88         88      88      88
88888888P"   `"YbbdP"'   `"YbbdP"'  88   `Y8a   `8'       `8'     `"YbbdP"'  88         88      88      88

Wellcome to BoookWorm
By aa224iu and fj222jy'''
print(intro)
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

