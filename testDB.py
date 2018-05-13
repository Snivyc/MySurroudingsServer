import sqlite3

conn = sqlite3.connect('date.db')
curs = conn.cursor()
curs.execute("select * from User")
print(curs.fetchall())
