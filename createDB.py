import sys
import os
import sqlite3

conn = sqlite3.connect('shakespearePlays.sqlite')
cur = conn.cursor()
conn.text_factory = str
#Drop tables if they already exist
cur.execute('''DROP TABLE IF EXISTS Plays ''')
cur.execute('''DROP TABLE IF EXISTS Characters ''')
cur.execute('''DROP TABLE IF EXISTS Speeches ''')
cur.execute('''DROP TABLE IF EXISTS Lines ''')

#Create Tables
cur.execute('''CREATE TABLE IF NOT EXISTS Plays 
    (id INTEGER PRIMARY KEY, name TEXT, characters INTEGER)''') 
cur.execute('''CREATE TABLE IF NOT EXISTS Characters
    (id INTEGER PRIMARY KEY, name TEXT, speeches)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Speeches
    (id INTEGER PRIMARY KEY, act INTEGER, number INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Lines
    (id INTEGER PRIMARY KEY, number INTEGER, words TEXT)''') 
    
#Insert play name into 
for fileName in os.listdir('.'):
    if fileName.lower().endswith('.txt'):
        fileName = fileName[:-4]
        cur.execute('''INSERT OR IGNORE INTO PLAYS (name)
            VALUES(?)''',(fileName,))
        print fileName, 
conn.commit()
cur.close()