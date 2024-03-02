import os
#web
# DB_URI = 'sqlite:////tmp/test.db'
DB_URI = 'mysql+pymysql://%s:%s@chall7-thelikebutton/%s' % (os.environ['MYSQL_USER'], os.environ['MYSQL_PASSWORD'], os.environ['MYSQL_DATABASE'])
print(DB_URI)
SECRET_KEY = os.environ['SECRETKEY']
HASH_ROUNDS = 1000
