import os
#web
# DB_URI = 'sqlite:////tmp/test.db'
DB_URI = 'mysql+pymysql://%s:%s@chall7-mktrace-db/%s' % (os.environ['MYSQL_USER'], os.environ['MYSQL_PASSWORD'], os.environ['MYSQL_DATABASE'])
print(DB_URI)
SECRET_KEY = os.urandom(10)
