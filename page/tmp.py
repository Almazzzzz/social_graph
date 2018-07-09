import uwsgi
import time
def loop():
    while True:
        message = uwsgi.mule_get_msg()
        print(message)
        time.sleep(10)

if __name__ == '__main__':
    loop()