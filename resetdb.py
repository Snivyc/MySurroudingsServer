import random
import sqlite3

db = sqlite3.connect('date.db',detect_types=sqlite3.PARSE_DECLTYPES)
db.row_factory = sqlite3.Row

with open('123.sql') as f:
    db.executescript(f.read())


pointLst = []
nameLst = ["火锅", "网吧"," 自助餐", "修电脑","通马桶","卖电脑","超市","便利店","理发店","菜场"]


i = 0
while i < 10:
    x=random.uniform(32.03,32.07)
    y=random.uniform(118.72,118.78)
    information = nameLst[i]
    db.execute(
        'INSERT INTO POINT (x,y,Information, author_id) VALUES (?, ?, ?, ?)',
        (x, y,information,1)
    )
    db.commit()
    i += 1