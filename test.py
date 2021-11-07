import collections
import sqlite3


db = sqlite3.connect("mastermind.db")
cur=db.cursor()

cur.execute("SELECT * FROM records")
result=cur.fetchall()
for row in result:
    print("first")
    print(row)
