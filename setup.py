import sqlite3

conn = sqlite3.connect("lab.db")

print("Database created")

conn.execute('''
CREATE TABLE words (
   ID INTEGER PRIMARY KEY,
   CONTENT TEXT NOT NULL
)
''')

print("Table `words` created")

conn.execute('''
CREATE TABLE urls (
   ID INTEGER PRIMARY KEY,
   URL TEXT NOT NULL
)
''')

print("Table `urls` created")

conn.execute('''
CREATE TABLE urls_words (
   ID INTEGER PRIMARY KEY,
   URL_ID INTEGER,
   WORD_ID INTEGER
)
''')

print("Table `urls_words` created")

conn.commit()
conn.close()
