def homeView(): # main menu/home page
    print('')
    print('Press 1: menage member')
    print('Press 2: manage book')
    print('Press 3: manage loan')
    print('Press 4: exit')
    return int(input('# '))

def bookView(): # book manu
    print('Press 1: add book')
    print('Press 2: edit book')
    print('Press 3: delete book')
    return int(input('# '))

def loanView():
    print('Press 1: add loan detail')
    print('Press 2: delete loan detail')
    return int(input('# '))

def addBook(): # add book
    name = input('[+] Name: ')
    author = input('[+] Author: ')
    edit = int(input('[+] Edition: '))
    bType = input('[+] Type: ')
    book = (name, author, edit, bType) # save as tuple
    return book

def invalidInput():
    print('[+] ERROR!: Invalid input')