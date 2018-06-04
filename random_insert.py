import random
import sqlite3

xing_str = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜"
xing_list = [i for i in xing_str]
nameLst = ["火锅", "网吧", "自助餐", "酒店", "修电脑", "卖电脑", "超市", "便利店", "理发店", "菜场"]

db = sqlite3.connect(
    'date.db',
    detect_types=sqlite3.PARSE_DECLTYPES
)
db.row_factory = sqlite3.Row

info_map = dict()
for i in range(1000):
    a = random.choice(xing_list)
    b = random.choice(nameLst)
    tstr = '小%s%s' % (a, b)
    info_map.setdefault(tstr, 0)
    info_map[tstr] = info_map[tstr] + 1
    if info_map[tstr] > 1:
        tstr = tstr + str(info_map[tstr])

    my_x = 32.33783
    my_y = 119.405099
    x = random.uniform(my_x  - 0.1, my_x + 0.1)
    y = random.uniform(my_y - 0.1, my_y + 0.1)
    print(tstr,x,y)

    db.execute(
        'INSERT INTO Point (author_id, X, Y, Information) VALUES (?, ?, ?, ?)',
        (1, x, y, tstr)
    )

db.commit()
db.close()