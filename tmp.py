import uwsgi
import time
from graph import *


def loop():
    while True:
        key = uwsgi.mule_get_msg()
        ids = key.decode('utf-8').split('_')
        uwsgi.cache_set(key, 'inprogress')
        try:
            result = bfs(ids[0], ids[1])
        except:
            uwsgi.cache_update(key, 'fail')
        else:
            if result:
                uwsgi.cache_update(key, 'found')
            else:
                uwsgi.cache_update(key, 'notfound')


if __name__ == '__main__':
    loop()
