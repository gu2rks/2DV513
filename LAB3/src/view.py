def homeView(): # main menu/home page
    print('')
    print('Press 1: manage member')
    print('Press 2: manage book')
    print('Press 3: manage loan')
    print('Press 4: exit')
    return int(input('# '))

def bookView(): # book manu
    print('Press 1: add book')
    print('Press 2: edit book')
    print('Press 3: delete book')
    return int(input('# '))

def memberView(): #member menu
    print('press 1: add member')
    print('press 2: delete member')
    print('press 3: edit member')
    return int(input('# '))

def loanView():
    print('Press 1: add loan detail')
    print('Press 2: delete loan detail')
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