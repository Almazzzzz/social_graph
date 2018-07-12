from flask import Flask, render_template, redirect, url_for, request, session
from flask import escape, make_response, Response
from app import app
import datetime
import json
import uwsgi
from vk_api_for_web import *


CURRENT_DATE = datetime.datetime.utcnow()


@app.route('/')
def index():
    if request.cookies.get('username'):
        return redirect(url_for('search_user'))
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    error = None
    service = VkApiForWeb(request.form['username'],
                          request.form['password'], with_app=True)
    vk_session = service.session
    error = service.error

    if error:
        return render_template('index.html', error=error)
    else:
        response = make_response(redirect(url_for('search_user')))
        expire_date = CURRENT_DATE + datetime.timedelta(days=1)
        response.set_cookie('username', request.form['username'],
                            expires=expire_date)
        return response
        return redirect(url_for('search_user'))


@app.route('/autocomplete')
def autocomplete():
    result = []
    term = request.args.get('term')
    username = request.cookies.get('username')
    service = VkApiForWeb(login=username)
    vk_session = service.session

    if service.error:
        return result
    else:
        api = vk_session.get_api()
        data = api.search.getHints(q=term, limit=40,
                                   fields='country, city, photo_50')
        result = autocomplete_data(data)

    return Response(json.dumps(result), mimetype='application/json')


@app.route('/search_user')
def search_user():
    username = request.cookies.get('username')
    service = VkApiForWeb(login=username)
    vk_session = service.session

    if service.error:
        return redirect(url_for('/'))
    else:
        api = vk_session.get_api()
        user_id = vk_session.check_sid()['user']['id']
        user = api.account.getProfileInfo()['first_name']

    return render_template('search_user.html', user=user, user_id=user_id)


@app.route('/data_handler', methods=['POST'])
def data_handler():
    success = False
    fails_messages = {
        'notfound': 'Увы, но общих знакомых нет',
        'fail': 'Увы, но общих знакомых нет',
        'inprogress': 'Поиск еще ведется, подождите'
    }

    user = request.form['user']
    user_id = request.form['user_id']

    if not request.form['search']:
        error = 'Нужно указать кого искать'
        return render_template('search_user.html', error=error,
                               user=user, user_id=user_id)

    username = request.cookies.get('username')
    service = VkApiForWeb(login=username)
    vk_session = service.session
    if service.error:
        return render_template('search_user.html', error=error,
                               user=user, user_id=user_id)
    api = vk_session.get_api()

    try:
        target_user = api.users.get(user_ids=str(request.form['search']))
    except:
        error = 'Пользователя не существует. Попробуйте другой запрос.'
        return render_template('search_user.html', error=error,
                               user=user, user_id=user_id)

    target_user_id = target_user[0].get('id')
    key = f'{str(user_id)}_{str(target_user_id)}'
    if uwsgi.cache_exists(key):
        cache_data = uwsgi.cache_get(key).decode('utf-8')
        if cache_data == 'found':
            message = 'Есть в кеше, идем в базу'
            success = True
            uwsgi.mule_msg(key) # Это и есть запрос запуск работы
        elif cache_data in list(fails_messages.keys()):
            # Говорим, что общих знакых нет
            message = fails_messages.get(cache_data)
            success = False
    else:
        message = 'Кеш пустой. Поищем в базе'
        uwsgi.mule_msg(key)

    return redirect(url_for('result', user_id=user_id, message=message,
                           target_user_id=target_user_id, success=success))


@app.route('/result')
def result():
    username = request.cookies.get('username')
    service = VkApiForWeb(login=username)
    vk_session = service.session
    api = vk_session.get_api()

    user_id = request.args.get('user_id')
    target_user_id = request.args.get('target_user_id')
    message = request.args.get('message')
    success = request.args.get('success')

    users = api.users.get(user_ids=f'{str(user_id)}, {str(target_user_id)}',
                          fields='photo_50', name_case='ins')
    user = users[0]
    target_user = users[1]

    return render_template('result.html', user=user, message=message,
                           target_user=target_user, success=success)
