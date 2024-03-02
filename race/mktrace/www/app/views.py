from werkzeug.datastructures import is_immutable
from . import app
from functools import wraps
from flask import request, make_response, session, abort, jsonify, render_template, redirect, g, url_for, flash
from .db import Market, User, db, Order, Market
import logging
import datetime
import time
from os import environ

l = logging.getLogger('mkt.views')
l.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')
last_cleanup = None

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'username' not in session:
            flash("You need to login!", 'info')
            return redirect(url_for('login'))
        return f(*args, **kws)
    return decorated_function

def market_authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'market' not in session:
            flash("You need to join or create a market!", 'info')
            return redirect(url_for('new_market'))
        return f(*args, **kws)
    return decorated_function


@authorize
@app.context_processor
def utility_processor():
    d = {'euro':0, 'coins': 0}
    if 'username' not in session or session['username'] is None:
        return d
    u = User.query.filter_by(username=session['username']).first()
    d['euro'] = u.euro/100
    d['coins'] = u.coins
    return d

def restore_money(u, o):
    if o.is_buy:
        u.euro += o.euro
    else:
        u.coins += o.coins
    db.session.commit()

def delete_obj(o):
    db.session.delete(o)
    db.session.commit()


def match_orders(order):
    orders = []
    user_euro = 0
    user_coins = 0
    exchange_rate = order.euro/order.coins
    if order.is_buy:
        to_filter = Order.query.filter_by(is_buy=False, market=order.market)
        to_sort = [o for o in to_filter if o.euro/o.coins <= exchange_rate]
        orders = sorted(to_sort, key=lambda o: o.euro/o.coins, reverse=False)
    else:
        to_filter = Order.query.filter_by(is_buy=True, market=order.market)
        to_sort = [o for o in to_filter if o.euro/o.coins >= exchange_rate]
        orders = sorted(to_sort, key=lambda o: o.euro/o.coins, reverse=True)
    for x in orders:
        rate = x.euro/x.coins
        l.debug("matched %r \n\txchrate=\t%.4f\n\trate=\t%.4f", x, exchange_rate, rate)
        l.debug('user: %r', x.user)
        if order.is_buy:
            euro_ammount = min(order.euro, x.euro)
            coins_ammount = int(euro_ammount * rate)

            user_euro -= euro_ammount
            x.user.euro += euro_ammount
            user_coins += coins_ammount

            order.euro -= euro_ammount
            order.coins = order.euro // exchange_rate

            x.euro -= euro_ammount
            x.coins = x.euro // rate

        else:
            coins_ammount = min(order.coins, x.coins)
            euro_ammount = coins_ammount // exchange_rate

            user_euro += euro_ammount
            user_coins -= coins_ammount
            x.user.coins += coins_ammount

            order.coins -= coins_ammount
            order.euro = int(order.coins * exchange_rate)
            x.coins -= coins_ammount
            x.euro = int(x.coins * rate)


        l.debug("after updates \n\t%r\n\t%r", x, order)
        l.debug('user: %r', x.user)
        if x.euro == 0 and not x.coins == 0:
            l.error("Rounding error %r, destroying coins", x)
            x.coins = 0
        if not x.euro == 0 and x.coins == 0:
            l.error("Rounding error %r, destroying money", x)
            x.euro = 0
        if x.euro == 0 and x.coins == 0:
            delete_obj(x)
        if order.euro == 0 or order.coins == 0:
            #no more order to look for
            break
    db.session.commit()
    return (order, user_euro, user_coins)

@app.route('/new_order', methods=['POST'])
@authorize
@market_authorize
def new_order():
    l.debug("new Order request: %r, %r", request, request.form)
    euro = int(request.form['euro'].strip())
    coins = int(request.form['coins'].strip())
    is_buy = request.form['buy'] == "buy"
    if euro <= 0 or coins <=0:
        flash("No free stuff on this market!", 'danger')
        return redirect(url_for('market'))
    u = User.query.filter_by(username=session['username']).first()
    m = u.market
    if is_buy and euro > u.euro:
            flash("Not enough €!", 'warning')
            return redirect(url_for('market'))
    elif not is_buy and coins > u.coins:
            flash("Not enough 🪙!", 'warning')
            return redirect(url_for('market'))
    o = Order(coins=coins, euro=euro, user=u, market=m, date=datetime.datetime.now(), is_buy=is_buy)
    o, euro_ammount, coins_ammount = match_orders(o)
    l.debug("after match %r %r %r %r", o, euro_ammount, coins_ammount, u)
    u.euro += euro_ammount
    u.coins += coins_ammount
    if o.coins != 0 and o.euro != 0:
        l.debug("extra order %r", o)
        if is_buy:
            if euro > u.euro:
                flash("Not enough €!", 'warning')
                return redirect(url_for('market'))
            u.euro -= euro
        else:
            if coins > u.coins:
                flash("Not enough 🪙!", 'warning')
                return redirect(url_for('market'))
            u.coins -= coins
        db.session.add(o)
    else:
        delete_obj(o)
    db.session.commit()
    return redirect(url_for('market'))


@app.route('/delete_order/<int:o_id>', methods=['GET'])
@authorize
@market_authorize
def delete_order(o_id):
    l.debug("Delete Order: %r", o_id)
    o = Order.query.filter_by(id=o_id).first()
    u = User.query.filter_by(username=session['username']).first()
    if o.user != u:
        flash("You can only delete your orders!", 'warning')
        return redirect(url_for('market'))
    restore_money(u, o)
    delete_obj(o)
    return redirect(url_for('market'))

@app.route('/market', methods=['GET'])
@authorize
@market_authorize
def market():
    m = Market.query.filter_by(name=session['market']).first()
    return render_template("market.html", orders=m.orders)

@app.route('/join_market', methods=['POST', 'GET'])
@authorize
def join_market():
    if 'market' in session:
        flash("You already joined a market!", 'warning')
        return redirect(url_for('market'))

    if request.method == 'GET':
        return render_template("new_market.html")

    l.debug("Join Market request: %r, %r", request, request.form)
    name = request.form['name'].strip()
    password = request.form['password'].strip()
    if name == "" or password == "":
        l.debug("invalid name or password: %s:%s", name, password)
        flash("name or password invalid!", 'danger')
        return redirect(url_for('new_market'))
    u = User.query.filter_by(username=session['username']).first()
    m = Market.query.filter_by(name=name).first()
    if m is not None:
        l.debug("Join Market, %s:%s", name, password)
        m.users.append(u)
        m.set_password(password)
        db.session.add(m)
        db.session.commit()
        session['market'] = name
        flash("Market joined!", 'success')
        return redirect(url_for('market'))
    flash("Market does not exists!", 'info')
    return redirect(url_for('new_market'))

@app.route('/new_market', methods=['POST', 'GET'])
@authorize
def new_market():
    if 'market' in session:
        flash("You already joined a market!", 'warning')
        return redirect(url_for('market'))

    if request.method == 'GET':
        return render_template("new_market.html")

    l.debug("New Market request: %r, %r", request, request.form)
    name = request.form['name'].strip()
    password = request.form['password'].strip()
    if name == "" or password == "":
        l.debug("invalid name or password: %s:%s", name, password)
        flash("name or password invalid!", 'danger')
        return redirect(url_for('new_market'))
    u = User.query.filter_by(username=session['username']).first()
    m = Market.query.filter_by(name=name).first()
    if m is None:
        l.debug("New Market, %s:%s", name, password)
        m = Market(name=name, date=datetime.datetime.now())
        m.users.append(u)
        m.set_password(password)
        o = Order(coins=100, euro=100, user=u, market=m, date=datetime.datetime.now())
        db.session.add(m)
        db.session.add(o)
        db.session.commit()
        session['market'] = name
        flash("New Market created!", 'success')
        return redirect(url_for('market'))
    flash("Market already exists!", 'info')
    return redirect(url_for('new_market'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    l.debug("Register request: %r, %r", request, request.form)
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    if username == "" or password == "":
        l.debug("invalid username or password: %s:%s", username, password)
        flash("username or password invalid!", 'danger')
        return redirect(url_for('register'))

    u = User.query.filter_by(username=username).first()
    if u is None:
        l.debug("New User, %s:%s", username, password)
        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        session['username'] = username
        flash("Registration completed!", 'success')
        return redirect(url_for('login'))
    flash("Username already exists!", 'info')
    return redirect(url_for('register'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    session.clear()
    l.debug("Login request: %r, %r", request, request.form)
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    u = User.query.filter_by(username=username).first()
    if u is not None and u.verify_password(password):
        l.debug("Logged in, %s:%s", username, password)
        session['username'] = username
        m = u.market
        l.debug("Market for %r is %r", u, m)
        if m is not None:
            session['market'] = m.name
        flash("Welcome back!", 'success')
        return redirect(url_for('market'))
    flash("login failed!", 'danger')
    return redirect(url_for('login'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return "Logout succesful!", 200

@app.route('/flag', methods=['GET'])
@authorize
def flag():
    u = User.query.filter_by(username=session['username']).first()
    if u is None:
        return "No user", 400
    if u.coins > 100:
        return environ['FLAG'], 200
    return "You need extra coins fo the flag", 400

@app.route('/')
def redirect_view():
    return redirect('/login')