from flask import Flask, url_for, render_template, request, redirect, session, Markup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

# import json
# import plotly
# import pandas as pd
# import numpy as np
# import plotly.graph_objs as go
import os


APPNAME = 'GWorld Spending'

app = Flask(__name__)
app.config.update(APPNAME=APPNAME,)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *


@app.route('/', methods=['GET', 'POST'])
def home():
    # Session control
    if not session.get('logged_in'):
        return render_template('index.html')
    else:

        if 'email' in session:
            name = session['email'].split("@")[0]

        # Implement loading bar here

        # myobj = Spending_History(session['email'], session['password'])
        # df = myobj.webpage_to_dataframe()

        return render_template('index.html', user=name)
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    # login form
    if request.method == 'GET':
        return render_template('login.html')
    else:
        _email = request.form['email']
        _pass = request.form['password']
        try:
            data = User.query.filter_by(email=_email, password=_pass).first()
            if data is not None:
                session['logged_in'] = True
                session['email'] = _email
                session['password'] = _pass
                return redirect(url_for('home'))
            else:
                return render_template("userError.html")
        except:
            return render_template("404.html")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    # registration form
    try:

        if request.method == 'POST':
            new_user = User(fname=request.form['fname'], lname=request.form['lname'],
                            email=request.form['email'], password=request.form['password'])
            db.session.add(new_user)
            db.session.commit()
            session['user'] = request.form['fname']

            return render_template('index.html')
    except exc.IntegrityError:
        return render_template("userError.html")

    return render_template('register.html')


@app.route('/logout/')
def logout():
    # logout form
    session['logged_in'] = False
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()