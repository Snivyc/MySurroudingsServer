import sqlite3

conn = sqlite3.connect('date.db')
curs = conn.cursor()
# curs.execute('DELETE FROM POINT WHERE id = 15')
curs.execute("select * from Point")
print(curs.fetchall())
curs.close()
conn.close()

