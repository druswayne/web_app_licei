from flask import Flask, render_template, request
import sqlite3

con = sqlite3.connect('data.db',check_same_thread=False)
cursor = con.cursor()
app = Flask(__name__)


@app.route('/date/<date>')
def get_page(date):
    print(date)
    cursor.execute(f'SELECT id, name,{date}  FROM UR_11')
    user_data = cursor.fetchall()
    print(user_data)
    return render_template('index.html', date=date,
                           data_user=user_data)


@app.route('/save/<date>')
def save_page(date):
    data = request.args
    for i in data:
        cursor.execute(f'UPDATE UR_11 set {date}={data.get(i)} WHERE id={i[3:]}')
        con.commit()
    return 'ok'


app.run(debug=True)
