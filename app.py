import json

from flask import Flask, render_template, request
import sqlite3
from json import dumps

con = sqlite3.connect('data.db', check_same_thread=False)
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
    start_index = index_date - 10
    if start_index < 0:
        start_index = 0
    return dumps(list_data[start_index:index_date] + list_data[index_date:index_date + 10])


@app.route('/date/')
def get_page():
    date = request.args.get('date')
    klass = request.args.get('klass')
    cursor.execute(f'SELECT id, name,{date}  FROM {klass}')
    user_data = cursor.fetchall()
    return render_template('index.html', date=date, klass=klass, data_user=user_data)


@app.route('/coin/')
def set_coin():
    date = request.args.get('date')
    klass = request.args.get('klass')
    cursor.execute(f'SELECT id, name,coin  FROM users')
    user_data = cursor.fetchall()
    return render_template('coin.html', date=date, klass=klass, data_user=user_data)


@app.route('/table/')
def get_table():
    data_table = []
    klass = request.args.get('klass')

    cursor.execute(f"""
        SELECT name
    FROM pragma_table_info('{klass}')
        """)
    list_data = ['№', 'ФИО']
    data = cursor.fetchall()
    for i in data:
        if i[0].startswith('date'):
            list_data.append(i[0])
    list_data.append('средний балл')
    cursor.execute(f'SELECT * FROM {klass}')
    user_data = cursor.fetchall()
    for user in user_data:
        data_table.append(user)
    for j in range(len(data_table)):
        sum = 0
        count_ = 0
        for i in range(2, len(data_table[j])):
            if isinstance(data_table[j][i], int):
                sum += data_table[j][i]
                count_ += 1
        try:
            data_table[j] += (round(sum / count_, 2),)
        except:
            data_table[j] += (0,)

    return render_template('table.html', data=data_table, top_data=list_data, klass=klass)


@app.route('/save_table/', methods=['POST'])
def save_table():
    klass = request.form['klass']

    cursor.execute(f"""
            SELECT name
        FROM pragma_table_info('{klass}')
            """)
    data = cursor.fetchall()
    list_data = []
    for i in data:
        if i[0].startswith('date'):
            list_data.append(i[0])
    data = request.form
    for i in data:
        if i != 'klass':
            name = i.split('_')[1]
            id_grade = int(i.split('_')[2])
            grade = data[i]
            cursor.execute(f"UPDATE {klass} set {list_data[id_grade - 1]} = (?) WHERE name=(?)", [grade, name])
    con.commit()
    return 'save ok'


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


@app.route('/save_coin/')
def save_coin():
    data = request.args
    print(data)
    for i in data:
        if i != "klass" and i != 'id_' and i != 'id_None':
            num = data.get(i)
            print(i)
            cursor.execute(f'UPDATE users set coin=(?) WHERE id={i[3:]}', [num])
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
        a = json.dumps(cursor.fetchall())

        return a


@app.route('/get_qwest/', methods=['post'])
def save_qwest():
    text_qwest = request.form['question_text']
    file_image = request.files.get('question_image')
    if file_image:
        file_image.save(f'/home/druswayne/mysite/static/uploads/{file_image.filename}')
        url_file = f'/static/uploads/{file_image.filename}'
    else:
        url_file = None
    correct_answer = request.form['correct_answer']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    question_hint = request.form['question_hint']
    data = {
        "text": text_qwest,
        "file_image": url_file,
        "correct_answer": int(correct_answer[-1]),
        "list_option": [option1, option2, option3, option4],
        "question_hint": question_hint

    }
    with open('/home/druswayne/mysite/static/qwest.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(data))
    return 'ok'


app.run(debug=True)
