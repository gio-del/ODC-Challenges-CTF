from flask import Flask
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 33768
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from .views import *
