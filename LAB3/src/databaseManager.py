import view as viewer  # import view

MEMBER = 'member'
BOOK = 'book'
LOAN = 'loan'
BORROW = 'borrow'
RETURNBOOK = 'return'

def bestReader (cursor):
        mySql_select_query = """Select concat(firstName, ' ', lastName) as MemberName, count(memID) as numberOfLaons
                            from `Member`
                            JOIN loanDetails on loanDetails.member_id = Member.memID
                            GROUP BY MemberName
                            HAVING numberOfLaons > 0
                            ORDER BY numberOfLaons DESC
                            """
        cursor.execute(mySql_select_query)
        records = cursor.fetchall() # need to change to fetch size 3
        print('The BEST READER (member that borrowed most books) during this period')                             
        count = 0
        for member in records:
            count = count + 1
            print('[RANK %d] Name: %s Totalt loan: %s' %(count, member[0], member[1]))
            if count == 3:
                break

def bestBooks(cursor):
    mySql_select_query = """Select name as bookName,author as bookAuthor, type as bookeType, edition as bookEd ,count(bkID) as numberOfLaons
                            from Book
                            JOIN LoanDetails on LoanDetails.book_id = Book.bkID
                            GROUP BY bookName,bookAuthor, bookeType,bookEd
                            HAVING numberOfLaons > 0
                            ORDER BY numberOfLaons DESC
                        """
    cursor.execute(mySql_select_query)
    records = cursor.fetchall() # need to change to fetch size 3
    print('The BEST BOOKS (most borrowed books) during this period')
    count = 0
    for book in records:
        count = count + 1
        print('[RANK %d] Book name: %s Totalt loan: %s\n\tAuthor: %s Type: %s Edition: %s' %(count,book[0], book[4], book[1], book[2], book[3]))
        if count == 3:
            break

def getMemberbyExpriedDay(cursor, date):
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
        if not isEmpty('exprie', records):
            print('Please remind these following members to return the borrowed books')
            for member in records:
                print('Name: %s %s' %(member[0], member[1]))

def isEmpty(op, item):
    if (len(item) == 0):  # the tuple is empty
        viewer.errorNotexist(op)
        return True
    else:
        return False

def getMemberId(cursor, personNum):
    mySql_select_query = "SELECT memID FROM `Member` WHERE personalNum = '%s' "
    cursor.execute(mySql_select_query, (personNum,))
    records = cursor.fetchall()
    return records

def getBookId(cursor, name, edition):
    mySql_select_query = "SELECT bkID FROM `Book` WHERE name = %s AND edition = %s"
    cursor.execute(mySql_select_query, (name, edition))
    records = cursor.fetchall()
    return records

"""
@op = opration code (book | member | loan)
@item = item that need to be add in database (tuples)
"""
def insertRecord(cursor, op, item):
    if(op == MEMBER):
        # note: member = (firstName, lastName, gender, address, personalNumn)
        mySql_insert_query = "INSERT IGNORE INTO `Member` (firstName, lastName, gender, address, personalNum) VALUES (%s, %s, %s, %s, %s)"
        val = (item[0], item[1], item[2], item[3], int(item[4]))
        cursor.execute(mySql_insert_query, val)
        print('[!] SUCESFUL: The MEMBER has been added into the database')
    elif (op == BOOK):
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

def deleteRecord(cursor, op, key):
    if(op == MEMBER):
        mySql_delete_query = "delete from `Member` where memID = '%s' "
        cursor.execute(mySql_delete_query, (key,))
        print('[!] SUCCESSFUL: The member has been deleted from database')
    elif(op == BOOK):
        mySql_delete_query = "delete from `Book` WHERE bkID = %s"
        cursor.execute(mySql_delete_query, (key,))
        print('[!] SUCCESSFUL: The book has been deleted from database')
    else:
        mySql_delete_query = "delete from `LoanDetails` WHERE book_id = %s AND member_id = %s"
        # memTodelete[0] = bookId [1] = memberId
        cursor.execute(mySql_delete_query,
                        (key[0], key[1]))
        print('[!] SUCCESSFUL: The loan detail has been deleted from database')

def updateRecord(cursor, op, key):
    if (op == MEMBER):
        member = viewer.addMember()
        mySql_update_query = "UPDATE `Member` SET firstName = %s, lastName = %s, gender = %s, address = %s, personalNum = %s where Member.memID = %s;"
        val = (member[0], member[1], member[2], member[3], int(member[4]), key)
        cursor.execute(mySql_update_query, val)
        print('[!] SUCESFUL: The MEMBER has been updated')
    elif (op == BOOK):
        book = viewer.addBook()
        mySql_update_query = "UPDATE Book SET name = %s, author = %s , edition = %s, type = %s where Book.bkID = %s;"
        val = (book[0], book[1], book[2], book[3], key)
        cursor.execute(mySql_update_query, val)
        print('[!] SUCESFUL: The BOOK has been updated')
    elif (op == BORROW):
        # borrow book -> decrease the stock
        mySql_update_query = "UPDATE Stock SET amount = amount - 1 where Stock.book_id = %s;"
        cursor.execute(mySql_update_query, (key, ))
    elif (op == RETURNBOOK):
        # return book -> increase the stock
        mySql_update_query = "UPDATE Stock SET amount = amount + 1 where Stock.book_id = %s;"
        cursor.execute(mySql_update_query, (key, ))

def getBorrowedBookByMember(cursor, key):
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

def stockHandler(cursor, op, bookId):
    mySql_select_query = "SELECT amount from bookStock where book_id = %s"
    cursor.execute(mySql_select_query, (bookId, ))
    records = cursor.fetchone()
    stock = int(records[0])
    if stock == 0:  # no book left in stock
        print('[!] Error: OUT OF STOCK\nThis book is not in the library at the moment')
        return False
    else:
        updateRecord(cursor, op, bookId)
        return True