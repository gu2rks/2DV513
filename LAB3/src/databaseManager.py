import view as viewer  # import view

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

