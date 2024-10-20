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
    return dumps(list_data[index_date-10:index_date]+list_data[index_date:index_date+10])

@app.route('/date/')
def get_page():
    date = request.args.get('date')
    klass = request.args.get('klass')
    cursor.execute(f'SELECT id, name,{date}  FROM {klass}')
    user_data = cursor.fetchall()
    return render_template('index.html', date=date,
                           data_user=user_data)




@app.route('/save/<date>')
def save_page(date):
    data = request.args
    for i in data:
        num = data.get(i)

        cursor.execute(f'UPDATE UR_11 set {date}=(?) WHERE id={i[3:]}', [num])
        con.commit()
    return 'изменения приняты'
app.run()