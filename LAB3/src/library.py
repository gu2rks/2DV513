import sys
import mysql.connector
import view as viewer #import view

class Controller:
    def __init__(self, mydb):
        while (True): 
            choice = viewer.homeView() # call main menu
            if (choice == 1):
                print('member')
            elif (choice == 2):
                self.bookHandler(mydb)
            elif (choice == 3):
                print('loan')
            elif (choice == 4):
                print('exit')
                sys.exit()
            else:
                viewer.invalidInput()

    def bookHandler(selft, mydb):
        choice = viewer.bookView()
        if (choice == 1):
            book = viewer.addBook()
            print(book)
        elif (choice == 2):
            print('edit')
        elif (choice == 3):
            print('delete')
        else:
            viewer.invalidInput()

#validate user input
if len(sys.argv) < 1:
    print('[+] ERROR: USECASE python3 library.py [password]')
    sys.exit()

try: # connecto the database
    mydb = mysql.connector.connect(
        host="localhost",
        user='root',
        passwd=str(sys.argv[1]),
        db='Library'
    )
except Exception as e:
    print(e)
    sys.exit("Can't connect to database")

controller = Controller(mydb) #create a Controller object
