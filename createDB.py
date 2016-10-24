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
    (id INTEGER PRIMARY KEY, name TEXT)''') 
cur.execute('''CREATE TABLE IF NOT EXISTS Characters
    (id INTEGER PRIMARY KEY, name TEXT, playID INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Speeches
    (id INTEGER PRIMARY KEY, act INTEGER, number INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Lines
    (id INTEGER PRIMARY KEY, number INTEGER, words TEXT)''') 
    
 
for fileName in os.listdir('.'):
    if fileName.lower().endswith('.txt'):
        fileName = fileName[:-4]
        #Insert play name into DB
        cur.execute('''INSERT OR IGNORE INTO PLAYS (name)
            VALUES(?)''',(fileName,))
        playKey = cur.lastrowid
        #Insert character names into DB
        fileName += ".txt"
        print fileName
        file=open(fileName,"r+")
        for word in file.read().split():
            word = word.lstrip('\'\"-,.:;!?]')
            word = word.rstrip('\'\"-,.:;!?]')  
            if word.isupper() and len(word) > 3 and word != "SCENE":  
                cur.execute('''SELECT COUNT(name) from CHARACTERS 
                                WHERE name = (?)''',(word,))
                if list(cur.fetchone())[0] < 1:
                    cur.execute('''INSERT OR IGNORE INTO CHARACTERS (name, 
                    playID) VALUES(?,?)''',(word, playKey,))
        print fileName, "added to database"
        
       
conn.commit()
cur.close()