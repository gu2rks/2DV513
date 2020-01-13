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
            members = self.getMemberId(cursor, personNum)
            if not self.isEmpty('member', members):  # check is member exist
                memberId = members[0]
                bookKey = viewer.getBookID()
                # book = (bookName, bookEdition)
                books = self.getBookId(cursor, bookKey[0], bookKey[1])
                if not self.isEmpty('book', books):  # check if book exist
                    bookId = books[0]
                    # check if the loanDetails is exist
                    if self.stockHandler(cursor, 'borrow', bookId[0]):
                         # get the first tuple
                        current = time.time()  # current time in unix time
                        threeWeek = 1814400  # three time in unix time
                        expired = current + threeWeek
                        expired = datetime.date.fromtimestamp(int(expired))
                        current = datetime.date.fromtimestamp(int(current))
                        # now insert loan detail
                        val = (current, expired, bookId[0], memberId[0])
                        self.insertRecord(cursor, 'loan', val)
            else:
                pass
        elif (choice == 2):
            print('Please enter following information to return the book')
            personNum = viewer.getPersonNum()
            # get member id by member.personNumber
            members = self.getMemberId(cursor, personNum)
            if not self.isEmpty('member', members):  # check is member exist
                memberId = members[0]
                bookKey = viewer.getBookID()
                books = self.getBookId(cursor, bookKey[0], bookKey[1])
                if not self.isEmpty('book', books):  # check if book exist
                    bookId = books[0]  # get the first tuple
                    mySql_select_query = "SELECT * FROM `LoanDetails` WHERE book_id = %s AND member_id = %s"
                    cursor.execute(mySql_select_query,
                                   (bookId[0], memberId[0]))
                    records = cursor.fetchall()
                    if not self.isEmpty('loan', records):
                        self.stockHandler(cursor, 'return', bookId[0])
                        self.deleteRecord(
                            cursor, 'loan', (bookId[0], memberId[0]))
        elif (choice == 3):
            exprie = viewer.exprie()
            date = datetime.date(int(exprie[0]), int(exprie[1]), int(exprie[2]))
            dbManager.getMemberbyExpriedDay(cursor,date)
        else:
            viewer.invalidInput()

    def stockHandler(self, cursor, op, bookId):
        mySql_select_query = "SELECT amount from bookStock where book_id = %s"
        cursor.execute(mySql_select_query, (bookId, ))
        records = cursor.fetchone()
        stock = int(records[0])
        if stock == 0:  # no book left in stock
            return False
            print(
                '[+] Error: OUT OF STOCK\nThis book is not in the library at the moment')
        else:
            self.updateRecord(cursor, op, bookId)
            return True

    def isEmpty(self, op, item):
        if (len(item) == 0):  # the tuple is empty
            viewer.errorNotexist(op)
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

    def getMemberbyExpriedDay(self, cursor, date):
        mySql_select_query = """
                            Select firstName, lastName
                            From `Member`
                            JOIN LoanDetails on Member.memID = LoanDetails.member_id
                            where expireDate in (
                                select expireDate
                                from LoanDetails
                                where expireDate = %s
                                )"""
        cursor.execute(mySql_select_query, (date,))
        records = cursor.fetchall()
        if not self.isEmpty('exprie', records):
            print('Please remind these following members to return the borrowed books')
            for member in records:
                print('Name: %s %s' %(member[0], member[1]))
        
    def bookHandler(self, cursor):
        choice = viewer.bookView()
        if (choice == 1):
            book = viewer.addBook()  # book as tuple
            self.insertRecord(cursor, "book", book)
        elif (choice == 2):
            print('delete')
        elif (choice == 3):
            book = viewer.getBookID()
            records = self.getBookId(cursor, book[0], book[1])
            if (not self.isEmpty('book', records)):
                bookId = records[0]
                self.updateRecord(cursor, 'book', bookId[0])            
        else:
            viewer.invalidInput()

    def memberHandler(self, cursor):
        choice = viewer.memberView()
        if(choice == 1):
            member = viewer.addMember()
            self.insertRecord(cursor, "member", member)
        else:
            personNum = viewer.getPersonNum()
            records = self.getMemberId(cursor, personNum)
            # check if member exist in database
            if (not self.isEmpty('member',records)):
                memberId = records[0]
                if(choice == 2):
                    self.deleteRecord(cursor, 'member', memberId[0])
                elif(choice == 3):
                    self.updateRecord(cursor, 'member', memberId[0])
                elif (choice == 4):
                    # check if member has borrow anybook
                    mySql_select_query = "SELECT * FROM `LoanDetails` WHERE member_id = %s"
                    cursor.execute(mySql_select_query, (memberId[0],))
                    records = cursor.fetchall()
                    if not self.isEmpty('loan', records):
                        self.getBorrowedBookByMember(cursor, personNum)
            else:
                viewer.invalidInput()
    
    def getBorrowedBookByMember(self, cursor, key):
        mySql_select_query = """
                            select *
                            From Book
                            where bkID in(
                                SELECT book_id
                                From LoanDetails
                                JOIN `Member` ON LoanDetails.member_id = Member.memID
                                WHERE personalNum = '%s'
                            )"""
        cursor.execute(mySql_select_query, (key,))
        records = cursor.fetchall()
        print('The following books have been borrow by this member')
        count = 0
        for book in records:
            count = count + 1
            print('%d Book name: %s \n\tAuthor: %s Edition: %s' %(count, book[1], book[2], book[3]))

    def updateRecord(self, cursor, op, key):
        if (op == 'member'):
            member = viewer.addMember()
            mySql_update_query = "UPDATE `Member` SET firstName = %s, lastName = %s, gender = %s, address = %s, personalNum = %s where Member.memID = %s;"
            val = (member[0], member[1], member[2], member[3], int(member[4]), key)
            cursor.execute(mySql_update_query, val)
            print('[!] SUCESFUL: The MEMBER has been updated')
        elif (op == 'book'):
            book = viewer.addBook()
            mySql_update_query = "UPDATE Book SET name = %s, author = %s , edition = %s, type = %s where Book.bkID = %s;"
            val = (book[0], book[1], book[2], book[3], key)
            cursor.execute(mySql_update_query, val)
            print('[!] SUCESFUL: The BOOK has been updated')
        elif (op == 'borrow'):
            # borrow book -> decrease the stock
            mySql_update_query = "UPDATE Stock SET amount = amount - 1 where Stock.book_id = %s;"
            cursor.execute(mySql_update_query, (key, ))
        elif (op == 'return'):
            # return book -> increase the stock
            mySql_update_query = "UPDATE Stock SET amount = amount + 1 where Stock.book_id = %s;"
            cursor.execute(mySql_update_query, (key, ))

    """
    @op = opration code (book | member | loan)
    @item = item that need to be add in database (tuples)
    """
    def insertRecord(self, cursor, op, item):
        if(op == 'member'):
            # note: member = (firstName, lastName, gender, address, personalNumn)
            mySql_insert_query = "INSERT IGNORE INTO `Member` (firstName, lastName, gender, address, personalNum) VALUES (%s, %s, %s, %s, %s)"
            val = (item[0], item[1], item[2], item[3], int(item[4]))
            cursor.execute(mySql_insert_query, val)
            print('[!] SUCESFUL: The MEMBER has been added into the database')

        elif (op == 'book'):
            # add book
            # note: book = (name, author, edit, bType)
            mySql_insert_query = 'INSERT IGNORE INTO Book (name, author, edition, type) VALUES (%s, %s, %s, %s)'
            val = (item[0], item[1], item[2], item[3])
            cursor.execute(mySql_insert_query, val)

            # add stock
            bookid = cursor.lastrowid  # get the id of just added book
            mySql_insert_query = 'INSERT IGNORE INTO Stock (amount, book_id) VALUES (%s, %s)'
            val = (item[4], bookid)
            cursor.execute(mySql_insert_query, val)
            print('[!] SUCCESSFUL: The stock has been added into the database')

        else:
            mySql_insert_query = 'INSERT IGNORE INTO `LoanDetails` (date, expireDate, book_id, member_id) VALUES (%s, %s, %s, %s)'
            cursor.execute(mySql_insert_query,
                           (item[0], item[1], item[2], item[3]))
            print('[!] SUCCESSFUL: The LOAN detail has been added into the database')

    """
    @op = opration code (book | member | loan)
    @keyTodelete = The key which will be use for searching for the object
    """

    def deleteRecord(self, cursor, op, keyTodelete):
        if(op == 'member'):
            mySql_delete_query = "delete from `Member` where personalNum = '%s' "
            cursor.execute(mySql_delete_query, (keyTodelete,))
            print('[!] SUCCESSFUL: The member has been deleted from database')
        elif(op == 'book'):
            print('delete book')
        else:
            mySql_delete_query = "delete from `LoanDetails` WHERE book_id = %s AND member_id = %s"
            # memTodelete[0] = bookId [1] = memberId
            cursor.execute(mySql_delete_query,
                           (keyTodelete[0], keyTodelete[1]))
            print('[!] SUCCESSFUL: The loan detail has been deleted from database')


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


controller = Controller(mydb)  # create a Controller
