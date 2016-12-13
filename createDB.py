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
cur.execute('''DROP TABLE IF EXISTS Words ''')

#Create Tables
cur.execute('''CREATE TABLE IF NOT EXISTS Plays 
    (id INTEGER PRIMARY KEY, name TEXT)''') 
cur.execute('''CREATE TABLE IF NOT EXISTS Characters
    (id INTEGER PRIMARY KEY, name TEXT, playID INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Speeches
    (id INTEGER PRIMARY KEY, speech TEXT, characterID INTEGER,
    act TEXT, number INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Lines
    (id INTEGER PRIMARY KEY, line TEXT, speechID, number INTEGER)''') 
cur.execute('''CREATE TABLE IF NOT EXISTS Words
    (id INTEGER PRIMARY KEY, word TEXT, lineID INTEGER)''') 
    
 
for fileName in os.listdir('.'):
    if fileName.lower().endswith('.txt'):
        playName = fileName[:-4]
        #Insert data into play table of DB
        cur.execute('''INSERT OR IGNORE INTO PLAYS (name)
            VALUES(?)''',(playName,))
        playKey = cur.lastrowid
        
        #Insert data into character table of DB
        file=open(fileName,"r+")
        for word in file.read().split():
            word = word.lstrip('\'\"-,.:;!?]')
            word = word.rstrip('\'\"-,.:;!?]')  
            if word.isupper() and len(word) > 3 and word != "SCENE" and word != "PRINCE":  
                # Check if character is already in database
                cur.execute('''SELECT COUNT(name) from CHARACTERS 
                                WHERE name = (?)''',(word,))
                if list(cur.fetchone())[0] < 1:
                    cur.execute('''INSERT OR IGNORE INTO CHARACTERS (name, 
                    playID) VALUES(?,?)''',(word, playKey,))
        
        # Insert data into speech table of DB
        file.seek(0)
        speech = ""
        character = ""
        speechNumber = 0
        lineNumber = 0
        newCharacter = False
        for line in file:      
            # Check if a new act is beginning
            if line.isupper() and line[0:3] == "ACT":
                act = line[3:].rstrip("\n")
            # Check if a new character is speeking
            if line.isupper() and line[0:3] != "ACT":
                if character != "" and characterID != None:
                    # Insert the previous speech into the DB
                    cur.execute('''INSERT OR IGNORE INTO SPEECHES (speech, 
                                characterID, act, number) 
                                VALUES(?,?,?,?)''', (speech, characterID[0], 
                                act, speechNumber, ))
                speechNumber += 1
                character = line.rstrip("\n")
                newCharacter = True
                speech = ""
            if line.isupper() == False and line[0:4] != "Exit" and line[0:5] != "Enter" and line != "\n":
                speech += " " + line       
                if newCharacter == True:
                    cur.execute(''' SELECT Characters.id 
                                    from CHARACTERS WHERE name = 
                                    (?)''', (character,))
                    characterID = cur.fetchone()
                    newCharacter == False
                try:
                    characterID            
                except: pass
                else:
                    if characterID != None:
                        lineNumber += 1
                        # Insert data into line table of DB
                        cur.execute('''INSERT OR IGNORE INTO LINES (line, 
                                    speechID, number) VALUES(?,?,?)''', 
                                    (line, speechNumber, lineNumber, ))  
                        words = line.split()
                        for word in words:
                            if word.isupper() == False:
                                cur.execute('''INSERT OR IGNORE INTO WORDS (word, 
                                        lineID) VALUES(?,?)''', (word, lineNumber, ))   
                            elif word.isupper() == True and len(word) < 2:
                                cur.execute('''INSERT OR IGNORE INTO WORDS (word, 
                                        lineID) VALUES(?,?)''', (word, lineNumber, )) 
        conn.commit()
        print fileName, "added to database"     

cur.close()