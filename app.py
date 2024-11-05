import json
from flask import Flask, render_template, request
import sqlite3
from json import dumps
con = sqlite3.connect('data.db',check_same_thread=False)
cursor = con.cursor()
app = Flask(__name__)


@app.route('/getdate/')
def get_date():
    date = request.args.get('date')
    klass = request.args.get('klass')
    list_data = []
    cursor.execute(f"""
    SELECT name
FROM pragma_table_info('{klass}')
    """)
    data = cursor.fetchall()
    for i in data:
        if i[0].startswith('date'):
            list_data.append(i[0])
    if date not in list_data:
        return dumps([])
    index_date = list_data.index(date)
    start_index = index_date-10
    if start_index < 0:
        start_index = 0
    return dumps(list_data[start_index:index_date]+list_data[index_date:index_date+10])

@app.route('/date/')
def get_page():
    date = request.args.get('date')
    klass = request.args.get('klass')
    cursor.execute(f'SELECT id, name,{date}  FROM {klass}')
    user_data = cursor.fetchall()
    return render_template('index.html', date=date, klass=klass, data_user=user_data)




@app.route('/save/<date>')
def save_page(date):
    data = request.args
    klass = data.get('klass')
    for i in data:
        if i != "klass":
            num = data.get(i)
            cursor.execute(f'UPDATE {klass} set {date}=(?) WHERE id={i[3:]}', [num])
            con.commit()
    return 'изменения приняты'

@app.route('/get_stats/')
def get_stat():
    data = request.args
    klass = data.get('klass')
    name = data.get('name')
    cursor.execute(f'SELECT * FROM {klass} WHERE name=(?)', [name])
    data_stats = cursor.fetchall()[0]
    list_stat = []
    for i in data_stats[2:]:
        if str(i).isdigit():
            list_stat.append(int(i))
    return json.dumps(list_stat)

@app.route('/get_data_db/')
def get_data_db():
    req = json.loads(request.args.get('request'))
    data = json.loads(request.args.get('data'))
    if req.lower().startswith('update') or req.lower().startswith('delete'):
        cursor.execute(req, data)
        con.commit()
        return json.dumps('ok')
    else:
        cursor.execute(req, data)
        a=json.dumps(cursor.fetchall())

        return a




app.run(debug=True)