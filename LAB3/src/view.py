def homeView(): # main menu/home page
    print('Press 1: Manage member')
    print('Press 2: Manage book')
    print('Press 3: Manage loan')
    print('Press 4: Get most read book (best book)')
    print('Press 5: Get best reader')
    print('Press 6: exit')
    return int(input('# '))

def bookView(): # book manu
    print('Press 1: Add book')
    print('Press 2: Delete book')
    print('Press 3: Edit book')
    return int(input('# '))

def memberView(): #member menu
    print('press 1: Add member')
    print('press 2: Delete member')
    print('press 3: Edit member')
    print('press 4: Get borrowed book by specific member')
    return int(input('# '))

def loanView():
    print('Press 1: Borrow book (Delete loan detail)')
    print('Press 2: Return book (Delete loan detail')
    print('Press 3: Get member info base on expried day')
    return int(input('# '))

def addBook(): # add book
    print('Please enter following information to add new book into the databse')
    name = input('Name: ')
    author = input('Author: ')
    edit = int(input('Edition: '))
    bType = bookType()
    stock = input('Stock/amount: ')
    book = (name, author, edit, bType, int(stock)) # save as tuple
    return book

def bookType():
    print('Please choose one of the following genres, for instance Press 7 for Fantasy book')
    print('1. Children \n2. Drama \n3. Fantasy \n4. Horror \n5. Romance \n6. Science fiction \n7. ETC')
    reps = input('#: ')
    if reps == 1:
        return 'Children'
    elif reps == 2:
        return 'Drama'
    elif reps == 3:
        return 'Fantasy'
    elif reps == 4:
        return 'Horror'
    elif reps == 5:
        return 'Romance'
    elif reps == 6:
        return 'Science fiction'
    else:
        return 'ETC'

def addMember(): # add member
    print('Please enter following information to add new member into the databse')
    firstName = input('first name: ')
    lastName = input('last neme: ')
    gender = genderValidate()
    address = input('adress: ')
    persNum = input('personal number in YYMMDDXXXX format: ')
    member = (firstName, lastName, gender, address, persNum)
    return member

def genderValidate():
    reps = input('Press 1: Female \nPress 1: Male\n# :')
    if reps == 1:
        return 'male'
    else:
        return 'female'
    

def getPersonNum(): # delete member
    personNum = int(input('Enter the member\'s personal number in YYMMDDXXXX format: '))
    return personNum

def getBookID():
    bookName = input('Enter the book\'s name: ')
    bookEdit = int(input('Enter the book\'s edition: '))
    return (bookName,bookEdit)

def invalidInput():
    print('[+] ERROR!: Invalid input')

def exprie():
    inputDate = input('Enter a date in YYYY-MM-DD format: ')
    year, month, day = inputDate.split('-')
    date = (year, month, day)
    return date

def errorNotexist(op):
    if (op == 'member'):
        print('[!] ERROR: Member is not exist in the database')
    elif (op == 'book'):
        print('[!] ERROR: Book is not exist in the database')
    elif (op == 'loan'):
        print('[!] ERROR: there is NO data about this specific loan in the database')
    elif (op == 'exprie'):
        print('[!] ERROR: there is loan that expried on that specific day')
    elif (op == 'personNum'):
        print('[!] ERROR: Invalid personal number, please put it YYMMDDXXX format')