import sqlite3

conn = sqlite3.connect('date.db')
curs = conn.cursor()
# curs.execute('DELETE FROM POINT WHERE id = 15')
curs.execute('SELECT * FROM POINT WHERE id = ?', (1011,))
print(curs.fetchall())
curs.close()
conn.close()

