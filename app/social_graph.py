from flask import Flask, render_template, redirect, url_for, request, session, escape, make_response, Response
from app import app
import vk_api
import datetime
import uwsgi
from vk_api_for_web import *
import settings

CURRENT_DATE = datetime.datetime.utcnow()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        service = VkApiForWeb(request.form['username'],
                              request.form['password'], with_app=True)
        vk_session = service.session

        error = service.error
        if not error:
            response = make_response(redirect(url_for('search_user')))
            expire_date = CURRENT_DATE + datetime.timedelta(days=1)
            response.set_cookie('username', request.form['username'],
                                expires=expire_date)
            return response

    if request.cookies.get('username'):
        return redirect(url_for('search_user'))

    return render_template('login.html', error=error)

@app.route('/search_user', methods=['GET', 'POST'])
def search_user():
    user = None
    info = None
    user_info_fn = None
    user_info_ln = None
    user_info_photo = None
    fails = {'notfound': 'Ничего не нашлось', 'fail': 'Ничего не нашлось',
             'inprogress': 'Поиск еще ведется, придите попозже'}

    username = request.cookies.get('username')
    service = VkApiForWeb(login=username)
    vk_session = service.session

    if service.error:
        return redirect(url_for('login'))
    else:
        curr_user_api = vk_session.get_api()
        user_id = vk_session.check_sid()['user']['id']
        user = curr_user_api.account.getProfileInfo()['first_name']

    if request.method == 'POST':
        if request.form['search']:
            try:
                user_info = curr_user_api.users.get(user_ids=str(request.form['search']),
                                                    fields='photo_50', name_case='acc')
                print(user_info)
            except:
                info = 'Нет такого, попробуй поискать кого-то еще'
            else:
                user_info_fn = user_info[0].get('first_name')
                user_info_ln = user_info[0].get('last_name')
                user_info_photo = user_info[0].get('photo_50')
                user_info_id = user_info[0].get('id')
                user_search = str(user_id) + '_' + str(user_info_id)
                if uwsgi.cache_exists(user_search):
                    cache_content = uwsgi.cache_get(user_search).decode('utf-8')
                    if cache_content in ['found']:
                        info = 'Есть в кеше, идем в базу'
                        uwsgi.mule_msg(user_search)
                    elif cache_content in list(fails.keys()):
                        info = fails.get(cache_content)
                    else:
                        info = 'Как ты сюда попал?'
                        print(cache_content)
                else:
                    info = 'Кеш пустой. Поищем в базе'
                    uwsgi.mule_msg(user_search)
            #curr_user_api.search.getHints(q=request.form['search'], limit=100, fields='country, city, photo_50')
        else:
            info = 'Нужно указать кого искать'

    return render_template('search_user.html', user=user, info=info, user_info_fn=user_info_fn,
                            user_info_ln=user_info_ln, user_info_photo=user_info_photo)
