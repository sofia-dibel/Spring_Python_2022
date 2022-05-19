# save this as app.py
import random
import time
from datetime import datetime

import flask
from flask import Flask, abort

app = Flask(__name__)
db = []
for i in range(3):
    db.append({
        'name': 'Anton',
        'time': 12343,
        'text': 'text01923097'
    })

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/send", methods= ['POST'])
def send_message():
    '''
    функция для отправки нового сообщения пользователем
    :return:
    '''
    data = flask.request.json
    if not isinstance(data, dict):
        return abort(400)

    if 'name' not in data or \
        'text' not in data:
        return abort(400)

    if not isinstance(data['name'], str) or \
        not isinstance(data['text'], str) or \
        len(data['name']) == 0 or \
        len(data['text']) == 0:
        return abort(400)

    text = data['text']
    name = data['name']

    if text[0] == '*':
        name = 'Анонимус'

    message = {
        'text': text,
        'name': name,
        'time': time.time()
    }

    if text == '/help':
        message['text'] = 'Начните сообщение со звездочки (*), чтобы отправить его анонимно. ' \
                          'Введите /password, если хотите поделиться надежным паролем с друзьями. ' \
                          'Введите /clear=name, если хотите удалить последнее сообщение пользователя name. ' \
                          'Введите /mymessages, если хотите узнать, сколько всего сообщений было вами отправлено. ' \
                          'Введите /imhere, если хотите узнать, когда вы здесь появились впервые'
        message['name'] = 'server'
        db.append(message)
    elif text == '/password':
        password = ''
        for i in range(12):
            password += chr(random.randint(33, 126))
        message['text'] = f'Ребята, хватайте хороший пароль, пока в наличии: {password}; новые не скоро завезут, вся эта ситуация в стране, сами понимаете...'
        db.append(message)
    elif text[:7] == '/clear=':
        n = text[7:]
        for i in range((len(db) - 1), -1, -1):
            if db[i]['name'] == n:
                db.pop(i)
                break
        message['text'] = f'{name} удалил(а) последнее сообщения пользователя {n}'
        message['name'] = 'server'
        db.append(message)
    elif text == '/mymessages':
        count = 0
        for i in db:
            if i['name'] == name:
                count += 1
        message['text'] = f'За всю историю этого мессенджера {name} отправила {count} сообщений(я)(е)'
        message['name'] = 'server'
        db.append(message)
    elif text == '/imhere':
        for i in db:
            if i['name'] == name:
                message['text'] = f'Я здесь с {datetime.fromtimestamp(i["time"]).strftime("%Y-%m-%d %H:%M:%S")}'
                break
        db.append(message)

    else:
        db.append(message)

    return {'ok': True}

@app.route("/messages")
def get_messages():
    try:
        after = float(flask.request.args['after'])
    except:
        abort(400)
    db_after = []
    for message in db:
        if message['time'] > after:
            db_after.append(message)
    return {'messages': db_after}

@app.route("/status")
def print_status():
    names = set()
    for i in db:
        names.add(i['name'])

    return f'Количество сообщений: {len(db)}, количество участников: {len(names)} ({", ".join(names)})'



app.run()