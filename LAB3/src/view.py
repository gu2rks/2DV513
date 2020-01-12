def homeView(): # main menu/home page
    print('')
    print('Press 1: manage member')
    print('Press 2: manage book')
    print('Press 3: manage loan')
    print('Press 4: exit')
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
    print('Press 1: Add loan detail')
    print('Press 2: Delete loan detail')
    print('Press 3: Get member info base on expried day')
    return int(input('# '))

def addBook(): # add book
    print('Please enter following information to add new book into the databse')
    name = input('[+] Name: ')
    author = input('[+] Author: ')
    edit = int(input('[+] Edition: '))
    bType = input('[+] Type: ')
    stock = input('[+] Stock:')
    book = (name, author, edit, bType, int(stock)) # save as tuple
    return book

def addMember(): # add member
    print('Please enter following information to add new member into the databse')
    firstName = input('[+] firstName: ')
    lastName = input('[+] lastName: ')
    gender = input('[+] gender: ')
    address = input('[+] adress: ')
    persNum = int(input('[+] persNum: '))
    member = (firstName, lastName, gender, address, persNum)
    return member

def getPersonNum(): # delet member
    memTodelete = int(input('Enter the member\'s personal number: '))
    return memTodelete

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