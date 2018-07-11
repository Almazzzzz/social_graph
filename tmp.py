import uwsgi
import time
def loop():
    while True:
        message = uwsgi.mule_get_msg()
        print(message.decode("utf-8").split('_')) #decode <class 'bytes'> to string and split to ['userID', 'searchUserID']
        uwsgi.cache_set(message, 'inprogress')
        time.sleep(10)
        uwsgi.cache_update(message, 'found')

if __name__ == '__main__':
    loop()