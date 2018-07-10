from flask import Flask, render_template, redirect, url_for, request, session, escape, make_response, Response
from app import app
import vk_api
import datetime
import uwsgi
import settings # app_id, client_secret

CURRENT_DATE = datetime.datetime.utcnow()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            sess = vk_api.VkApi(app_id=settings.vk_app, client_secret=settings.vk_key,
                                login=request.form['username'], password=request.form['password'],
                                scope='users, friends', api_version='5.80')
            try:
                sess.auth(token_only=True)
            except vk_api.exceptions.AuthError:
                error = 'Authorization error'
            except:
                error = 'Some error. Try again'
            else:
                #session['username'] = request.form['username']
                resp = make_response(redirect(url_for('hello')))
                expire_date = CURRENT_DATE + datetime.timedelta(days=1)
                resp.set_cookie('username', request.form['username'], expires=expire_date)
                return resp
        else:
            error = 'Empty Credentials. Please try again.'
    if request.cookies.get('username'):
        return redirect(url_for('hello'))
    return render_template('login.html', error=error)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    error = None
    cache = None
    fails = {'notfound': 'Ничего не нашлось', 'fail': 'Ничего не нашлось', 'inprogress': 'Поиск ещё ведется'}
    login = vk_api.VkApi(login=request.cookies.get('username'), scope='users, friends, groups')
    try:
        login.auth()
    except:
        return redirect(url_for('login'))
    else:
        curr_user_api = login.get_api()
        user_id = login.check_sid()['user']['id']
        user = curr_user_api.account.getProfileInfo()['first_name']

    if request.method == 'POST':
        if request.form['search']:
            user_search = str(user_id) + '_' + str(request.form['search'])
            if uwsgi.cache_exists(user_search):
                cache_content = uwsgi.cache_get(user_search).decode("utf-8")
                if cache_content in ['found']:
                    error = 'Есть в кеше, идём в бвзу'
                    uwsgi.mule_msg(user_search)
                elif cache_content in list(fails.keys()):
                    error = fails.get(cache_content)
                else:
                    error = 'Никуда не попал'
                    print(cache_content)
            else:
                error = 'Кеш пустой. Поищем в базе'
                uwsgi.mule_msg(user_search)
            #curr_user_api.search.getHints(q=request.form['search'], limit=100, fields='country, city, photo_50')
        else:
            error = 'Нужно указать кого искать'

    return render_template('hello.html', user=user, error=error, cache=cache)
