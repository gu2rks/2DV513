# Wellcome to bookWorm the application for library DBMS

## Structure
The application consit of 3 files:
1. library.py: the main class that act as a controller which communicate with the view.py and databaseManager.py
2. databaseManager.py: the backend which execute all sql querie.
3. view.py: take input from the user and send it to the controller. Also, output results to the user. 

## Requriment:
- python3
- MySQL Workbench
- mysql-connector-python by run ```pip3 install mysql-connector-python```
- database in ```/dump/dump.sql```

## How to run the application:
1. Make sure that you install the database by run ```dump.sql``` in MySQL Workbench
2. ```python3 src/library.python xxxxx``` Where **xxxxx** is your password to sql.
3. That is it! good luck, have fun