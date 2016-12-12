import sys
import os
import sqlite3

conn = sqlite3.connect('shakespearePlays2.sqlite')
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
    (id INTEGER PRIMARY KEY, speech TEXT, characterID INTEGER,
    act TEXT, number INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Lines
    (id INTEGER PRIMARY KEY, line TEXT, characterID INTEGER, 
    speechID, act TEXT, number INTEGER)''') 
cur.execute('''CREATE TABLE IF NOT EXISTS Words
    (id INTEGER PRIMARY KEY, characterID INTEGER, playID INTEGER, speechID,
    lineID INTEGER, act TEXT, number INTEGER)''') 
    
 
for fileName in os.listdir('.'):
    if fileName.lower().endswith('.txt'):
        playName = fileName[:-4]
        #Insert data into play table of DB
        cur.execute('''INSERT OR IGNORE INTO PLAYS (name)
            VALUES(?)''',(playName,))
        playKey = cur.lastrowid
           
        character = ""
        speech = ""
        speechNumber = 0
        lineNumber = 0
        newCharacter = False
        file=open(fileName,"r+")
        for line in file:   
            if line.isupper():
                for word in line.split():
                    word = word.lstrip('\'\"-,.:;!?]')
                    word = word.rstrip('\'\"-,.:;!?]')  
                    if len(word) > 3 and word != "SCENE" and word != "PRINCE": 
                        character = word
                        # Check if character is already in database
                        cur.execute('''SELECT COUNT(name) from CHARACTERS 
                                        WHERE name = (?)''',(character,))
                        if list(cur.fetchone())[0] < 1:
                            #Insert new character into character table of DB
                            cur.execute('''INSERT OR IGNORE INTO CHARACTERS (name, 
                            playID) VALUES(?,?)''',(character, playKey,))
            if line.isupper() and line[0:3] == "ACT":
                act = line[3:].rstrip("\n")
            
            # Check if a new character is speeking
            elif line.isupper() and line[0:3] != "ACT":
                # Get the character ID of the newCharacter
                cur.execute(''' SELECT Characters.id 
                                from CHARACTERS WHERE name = 
                                (?)''', (character,))
                characterID = cur.fetchone()
                if character != "" and characterID != None:
                    # Insert the previous speech into the DB
                    cur.execute('''INSERT OR IGNORE INTO SPEECHES (speech, 
                                characterID, act, number) 
                                VALUES(?,?,?,?)''', (speech, characterID[0], 
                                act, speechNumber, ))
                    lines = speech.split("\n")
                    #print lines
                    #for line in lines:
                        
                speechNumber += 1
                character = line.rstrip("\n")
                newCharacter = True
                speech = ""
            if line.isupper() == False:
                speech += " " + line              
                if newCharacter == True:
                    # Get the character ID of the newCharacter
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
                                    characterID, act, number) 
                                    VALUES(?,?,?,?)''', (line, characterID[0], 
                                    act, lineNumber, )) 
        conn.commit()
        print fileName, "added to database"     

cur.close()