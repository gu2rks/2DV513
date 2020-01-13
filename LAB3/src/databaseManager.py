import view as viewer  # import view

MEMBER = 'member'
BOOK = 'book'
LOAN = 'loan'

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
