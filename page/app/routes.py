from flask import Flask, render_template, redirect, url_for, request
from app import app

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('hello'))
    return render_template('login.html', error=error)

@app.route('/hello')
def hello():
    user = {'username': 'BlaBlahin'}
    return render_template('hello.html', title='Home', user=user)