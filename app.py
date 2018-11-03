from flask import Flask, flash, render_template, request, redirect, url_for, session, abort
import stripe
import os
import numpy as np
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *


app = Flask(__name__)

pub_key = 'pk_test_SF586n7bKRisyBDkWxVyTrbL'
stripe.api_key = 'sk_test_TMqJO4DLuAnqqSHRJsVwePH9'

@app.route('/')
def index():
    barista_flag = np.load('barista_flag.npy')[0]

    if barista_flag == 1:
        # Open JSON menu
        with open('menu/hot_drinks.json') as f:
            hot_drinks = json.load(f)
        order = ["Hot Coffees","Hot Teas","Other"]
        return render_template('index.html', pub_key=pub_key, food_items=hot_drinks, order=order)

    else:
        return redirect(url_for('closed'))

@app.route('/cold')
def cold():
    barista_flag = np.load('barista_flag.npy')[0]

    if barista_flag ==1:
        # Open JSON menu
        with open('menu/cold_drinks.json') as f:
            cold_drinks = json.load(f)
        order = ["Iced Coffees","Iced Teas","Lemonades"]
        return render_template('index.html',pub_key=pub_key,food_items=cold_drinks,order=order)

    else:
        return redirect(url_for('closed'))

@app.route('/food')
def food():
    barista_flag = np.load('barista_flag.npy')[0]

    if barista_flag == 1:
        # Open JSON menu
        with open('menu/food.json') as f:
            food = json.load(f)
        order = ["Savory","Sweet"]
        return render_template('index.html',pub_key=pub_key,food_items=food,order=order)

    else:
        return redirect(url_for('closed'))

@app.route('/closed')
def closed():
    return render_template('closed.html')

@app.route('/barista')
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # Create barista login flag
        np.save("barista_flag",np.array([1]))

        # Get orders from database
        engine = create_engine('sqlite:///drinks.db', echo=True)
        DBSession = sessionmaker(bind=engine)
        dbsession = DBSession()

        data = dbsession.query(User).all()
        drinks = []
        for row in data:
            drinks.append([row.id,row.name])

        return render_template('dashboard.html', drinks=drinks) # Barista dash

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == '1000calories' and request.form['username'] == 'thinmint':
        session['logged_in'] = True
        return redirect(url_for('login'))

    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False

    # Clear barista flag
    np.save("barista_flag",np.array([0]))

    return redirect(url_for('login'))

@app.route("/refresh", methods=['POST'])
def update():
    print(" \n Removing \n ", request.form['id'])
    id_to_remove = int(request.form['id'])

    # Remove from database
    engine = create_engine('sqlite:///drinks.db', echo=True)
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()
    drink = dbsession.query(User).get(id_to_remove)
    print(" Removing drink: ", drink)
    dbsession.delete(drink)
    dbsession.commit()

    # Get database data
    data = dbsession.query(User).all()
    drinks = []
    for row in data:
        drinks.append([row.id,row.name])
    dbsession.close()

    return redirect(url_for('login')) # Barista dash

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/pay200', methods=['POST'])
def pay200():
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=200,
        currency='usd',
        description='Cabot Cafe'
    )
    print("\n pay 200 \n")
    return redirect(url_for('thanks'))

@app.route('/pay250', methods=['POST'])
def pay250():
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=250,
        currency='usd',
        description='Cabot Cafe'
    )
    print("\n pay 250 \n")
    return redirect(url_for('thanks'))

@app.route('/pay300', methods=['POST'])
def pay300():
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=300,
        currency='usd',
        description='Cabot Cafe'
    )
    print("\n pay 300 \n")
    return redirect(url_for('thanks'))

@app.route('/pay350', methods=['POST'])
def pay350():
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=350,
        currency='usd',
        description='Cabot Cafe'
    )
    print("\n pay 350 \n")
    return redirect(url_for('thanks'))

@app.route('/pay400', methods=['POST'])
def pay400():
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=400,
        currency='usd',
        description='Cabot Cafe'
    )
    print("\n pay 400 \n")
    return redirect(url_for('thanks'))

@app.route('/pay450', methods=['POST'])
def pay450():
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=450,
        currency='usd',
        description='Cabot Cafe'
    )
    print("\n pay 450 \n")
    return redirect(url_for('thanks'))

@app.route('/pay500', methods=['POST'])
def pay500():
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=500,
        currency='usd',
        description='Cabot Cafe'
    )
    print("\n pay 500 \n")
    return redirect(url_for('thanks'))

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
