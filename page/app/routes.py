from flask import Flask, render_template, redirect, url_for, request
from app import app

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            session = vk.AuthSession('6615751', request.form['username'], request.form['password'], scope='users, friends')
            vk_api = vk.API(session, v='5.80')
            user = vk_api.users.get(user_ids='0')
            friends = vk_api.friends.get(user_id='0')
            print(friends)
            print(user)
        else:
            return redirect(url_for('hello'))
    return render_template('login.html', error=error)

@app.route('/hello')
def hello():
    user = {'username': 'BlaBlahin'}
    return render_template('hello.html', title='Home', user=user)