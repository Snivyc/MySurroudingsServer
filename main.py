import sqlite3
import functools
from math import radians, fabs, cos, sin, sqrt, asin

from flask import Flask, send_file, jsonify, Response, url_for, request, session, g

app = Flask(__name__)

EARTH_RADIUS=6371           # 地球平均半径，6371km

def hav(theta):
    s = sin(theta / 2)
    return s * s

def get_distance_hav(lat0, lng0, lat1, lng1):
    '''用haversine公式计算球面两点间的距离。'''
    # 经纬度转换成弧度
    lat0, lng0, lat1, lng1 = map(radians, [lat0, lng0, lat1, lng1])
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    return distance

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'date.db',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# @app.before_request
# def load_logged_in_user():
#     user_id = session.get('user_id')
#
#     if user_id is None:
#         g.user = None
#     else:
#         g.user = get_db().execute(
#             'SELECT * FROM user WHERE id = ?', (user_id,)
#         ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user_id = int(request.form['ID'])
        user = get_db().execute(
            'SELECT * FROM user WHERE AccountID = ?', (user_id,)
        ).fetchone()
        if user is None:
            return "false"
        return view(**kwargs)

    return wrapped_view
# @app.route('/test/')
# def test():
#     print('fuck')
#     s = ['张三', '年龄', '姓名']
#     return url_for('static', filename='test.json')
#     # return send_file('test.json')

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
    # if True:
        x = float(request.form['x'])
        y = float(request.form['y'])
        # x=32.05
        # y=118.75
        dx = 2/111.7
        dy = 2/(111.7 * cos(radians(x)))
        # print(dx, dy, cos(radians(x)))
        db = get_db()
        temp = db.execute(
            'SELECT * FROM POINT WHERE X < ? AND X > ? AND Y < ? AND Y > ?',(x+dx, x-dx, y+dy, y-dy)
        ).fetchall()
        lst = []

        def cal_distance(_x, _y):
            return get_distance_hav(x, y, _x, _y)

        for i in temp:
            distance = cal_distance(i["x"], i["y"])
            if distance < 2:
                lst.append({"x":i["x"], "y":i["y"], "information": i["information"], "distance": int(distance*1000)})
        lst.sort(key=lambda t : t["distance"])
        # print(lst[0:10])
    # return Response('test.json',mimetype='application/json')
    # print(url_for('static', filename='test.json',))
    # return url_for('static', filename='test.json',)

        return jsonify(lst)
    return send_file('static/test.json',mimetype='application/json')

@app.route('/search/<keyword>', methods=['GET', 'POST'])
@login_required
def search(keyword):
    if request.method == 'POST':
        x = float(request.form['x'])
        y = float(request.form['y'])
        dx = 2/111.7
        dy = 2/(111.7 * cos(radians(x)))
        # print(dx, dy, cos(radians(x)))
        db = get_db()
        temp = db.execute(
            'SELECT * FROM POINT WHERE Information LIKE ? AND X < ? AND X > ? AND Y < ? AND Y > ?' , ("%"+keyword+"%",x+dx, x-dx, y+dy, y-dy)
        ).fetchall()
        lst = []
        def cal_distance(_x, _y):
            return get_distance_hav(x, y, _x, _y)


        for i in temp:
            distance = cal_distance(i["x"], i["y"])
            if distance < 2:
                lst.append({"x":i["x"], "y":i["y"], "information": i["information"], "distance": int(distance*1000)})
        lst.sort(key=lambda t : t["distance"])
        # print(lst[0:10])
    # return Response('test.json',mimetype='application/json')
    # print(url_for('static', filename='test.json',))
    # return url_for('static', filename='test.json',)

        return jsonify(lst)
    return keyword

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE account = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif user['password']!=password:
            error = 'Incorrect password.'

        if error is None:

            return jsonify({'isSuccess':True, 'ID':user["AccountID"]})


    return jsonify({'isSuccess':False})

    # if request.method == 'POST':
    #     if request.form['username'] == 'admin' and request.form['password'] == '123456':
    #         return jsonify({'isSuccess':True})
    # return jsonify({'isSuccess':False})


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        account = request.form['account']
        password = request.form['password']
        db = get_db()
        error = None

        if not account:
            error = 'Account is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT AccountID FROM user WHERE Account = ?', (account,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(account)

        if error is None:
            db.execute(
                'INSERT INTO user (account, password) VALUES (?, ?)',
                (account, password)
            )
            db.commit()
            return jsonify({'isSuccess': True, 'errorInformation': ""})
        return jsonify({'isSuccess': False, 'errorInformation': error})

    return jsonify({'isSuccess':False, 'errorInformation':"不接受get"})


@app.route('/submitinfo', methods=['GET', 'POST'])
@login_required
def submitinfo():

    if request.method == 'POST':

        ID = request.form['ID']
        # password = request.form['password']
        info = request.form['info']
        x = float(request.form['x'])
        y = float(request.form['y'])
        db = get_db()
        error = None

        if not info:
            error = 'info is required'

        # if not account:
        #     error = 'Account is required.'
        # elif not password:
        #     error = 'Password is required.'
        # elif db.execute(
        #         'SELECT AccountID FROM user WHERE Account = ?', (account,)
        # ).fetchone() is not None:
        #     error = 'User {} is already registered.'.format(account)

        if error is None:
            db.execute(
                'INSERT INTO Point (author_id, X, Y, Information) VALUES (?, ?, ?, ?)',
                (ID, x, y, info)
            )
            db.commit()
            return jsonify({'isSuccess': True, 'errorInformation': ""})
        return jsonify({'isSuccess': False, 'errorInformation': error})

    return jsonify({'isSuccess':False, 'errorInformation':"不接受get"})

app.run(host='0.0.0.0', port=8080)

# app.run(port=8080)

