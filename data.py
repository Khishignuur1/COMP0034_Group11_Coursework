"""
Written by Khishignuur
"""


import sqlite3


def create_db():
    mydb = sqlite3.connect('data.sqlite')

    c = mydb.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS user (
                     id INTEGER NOT NULL PRIMARY KEY, 
                     name TEXT, 
                     email TEXT UNIQUE,
                     password TEXT, 
                     user_type VARCHAR(10) NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS item (
                     id INTEGER NOT NULL PRIMARY KEY, 
                     title TEXT, 
                     date_created TEXT UNIQUE,
                     content TEXT,
                     color TEXT,
                     size TEXT,
                     price  INTEGER NOT NULL,
                     user_id INT NOT NULL,
                     FOREIGN KEY(user_id) REFERENCES user(id))''')

    mydb.commit()



