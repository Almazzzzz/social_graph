from flask import Flask, render_template, redirect, url_for, request, session, escape
from app import app
import vk

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            try:
                session = vk.AuthSession('6615751', request.form['username'], request.form['password'], scope='users, friends')
            except vk.exceptions.VkAuthError:
                error = 'Authorization error'
            except:
                error = 'Some error. Try again'
            else:
                vk_api = vk.API(session, v='5.80')
                user = vk_api.account.getProfileInfo()
                error = user #временно для проверки что хранится в user.
 #               return redirect(url_for('hello'))
        else:
            error = 'Empty Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/hello')
def hello():
    user = {'username': 'BlaBlahin'}
    return render_template('hello.html', title='Home', user=user)