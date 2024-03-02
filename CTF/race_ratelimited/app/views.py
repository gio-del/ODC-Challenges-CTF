from flask import session, render_template, request, redirect, url_for, flash, abort, jsonify
from hashlib import sha3_512
import time
import math
import os
from string import ascii_letters
from functools import wraps

from . import app
from .db import Message, User, Like, db
import logging
l = logging.getLogger(__name__)
l.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')

last_reset = 0
TIME_OUT = 10
# 10h rate limit
RATE_LIMIT_TIME = 10*60*60
NUM_LIKES = 3

flag_likes = os.environ['FLAG']
RATE_LIMIT_CACHE = {}

def get_current_user():
    current_user = None
    if 'user' in session:
        current_user = User.query.filter_by(username=session['user']).first()
    return current_user


def compute_hash(s, maxval):
    r = 0
    for c in s:
        r += ord(c)
    return r % maxval

@app.before_request
def initapp():
    global last_reset
    if last_reset+TIME_OUT < time.time():
        # TODO: reset the app
        last_reset = time.time()
        db.create_all()
        RATE_LIMIT_CACHE.clear()

@app.template_filter('ctime')
def timectime(s):
    return time.ctime(s)

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'user' not in session:
            flash("You need to login!", 'info')
            return redirect(url_for('login'))
        return f(*args, **kws)
    return decorated_function

@app.route('/')
@authorize
def index():
    u = get_current_user()
    if u is not None and u.got_tons_like:
        flash("You got tons of likes: %s" % flag_likes, 'success')

    posts = Message.query.order_by(Message.time.desc()).all()
    return render_template('index.html', current_user=u, posts=posts, lenp=len(posts))

@app.route('/post', methods=['GET', 'POST'])
@authorize
def post():
    u = get_current_user()
    if u is None:
        flash("You need to log in first.", 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        content = request.form.get('content', '')
        img = request.form.get('img', '')

        if content == "":
            flash("You cannot send an empty message!")
        elif img == "":
            flash("You need to send a image url!")
        else:
            m = Message(sender=u, content=content, img=img, time=int(time.time()))
            db.session.add(m)
            db.session.commit()
            flash("You posted a new picture!")
        return redirect(url_for('index'))
    return render_template('private.html', current_user=u)

def check_rate_limit(u, p):
    likes = Like.query.filter_by(user=u, message=p).order_by(Like.date.desc()).all()
    time_limit = time.time() - RATE_LIMIT_TIME
    for l in likes:
        if l.date > time_limit:
            return True
    return False

@app.route('/like', methods=['POST'])
@authorize
def like():
    u = get_current_user()
    if u is None:
        flash("You need to log in first.", 'danger')
        return redirect(url_for('login'))
    msg_id = int(request.form.get('message_id', '-1'))

    if msg_id >= 0:
        p = Message.query.filter_by(id=msg_id).first()
        # rate_limit_check = time.time() - RATE_LIMIT_CACHE.get(p, time.time()-100) < 10
        rate_limit_check = check_rate_limit(u, p)

        l.info("like request: %r, %r, %r", request, request.form, p)
        if p is not None and p.sender_id == u.id:
            # rate limit the likes
            if rate_limit_check:
                flash("You are liking too fast!")
                return redirect(url_for('index'))
            l.info("like request: %r, %r, %r", request, request.form, p)
            like = Like(user=u, message=p, date=int(time.time()))
            db.session.add(like)
            flash("You liked a post!")
            if len(p.likes) > NUM_LIKES:
                p.sender.got_tons_like = True
            RATE_LIMIT_CACHE[p] = time.time()
            db.session.commit()
        else:
            flash("You cannot like other's post!")
    return redirect(url_for('index'))

@app.route('/unlike', methods=['POST'])
@authorize
def unlike():
    u = get_current_user()
    if u is None:
        flash("You need to log in first.", 'danger')
        return redirect(url_for('login'))

    flash("You want to unliked a post bhooo!")
    return redirect(url_for('index'))




@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash("Logout succesful!", 'success')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        get_current_user()
        return render_template('login.html')

    elif request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        login = request.form.get('login', '')
        register = request.form.get('register', '')
        if login == "login":
            session.clear()
            l.debug("Login request: %r, %r", request, request.form)
            u = User.query.filter_by(username=username).first()
            if u is not None and u.verify_password(password):
                l.debug("Logged in, %s:%s", username, password)
                session['user'] = username
                flash("Welcome back!", 'success')
                return redirect(url_for('index'))
            flash("login failed!", 'danger')
            return redirect(url_for('login'))

 
        elif register == "register":
            l.debug("Register request: %r, %r", request, request.form)
            if username == "" or password == "":
                l.debug("invalid username or password: %s:%s", username, password)
                flash("username or password invalid!", 'danger')
                return redirect(url_for('login'))
            for c in username:
                if c not in ascii_letters:
                    l.debug("invalid characters in username: %s", username)
                    flash("invalid characters in username!", 'danger')
                    return redirect(url_for('login'))

            u = User.query.filter_by(username=username).first()
            if u is None:
                l.debug("New User, %s:%s", username, password)
                u = User(username=username)
                u.set_password(password)
                db.session.add(u)
                db.session.commit()
                session['username'] = username
                flash("Registration completed!", 'success')
                return redirect(url_for('index'))
            flash("Username already exists!", 'info')
            return redirect(url_for('login'))
        else:
            flash('There was something wrong about last request I got.')
        return redirect(url_for('index'))
