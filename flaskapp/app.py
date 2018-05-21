import json
import plotly
import pandas as pd
import numpy as np
import plotly.graph_objs as go

from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

import stats
from spending import Spending_History

APPNAME = 'GWorld Spending'
app = Flask(__name__)
app.config.update(APPNAME=APPNAME,)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = "123"
db = SQLAlchemy(app)


class User(db.Model):
    # Create the user table
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, fname, lname, email, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password


class History(db.Model):
    # create the spending history table
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer)
    account = db.Column(db.Text)
    time = db.Column(db.Integer)
    vendor = db.Column(db.Text)
    price = db.Column(db.Float)
    email = db.Column(db.String(100), db.ForeignKey('user.email'))

    def __init__(self, date, account, time, vendor, price, email):
        self.date = date
        self.account = account
        self.time = time
        self.vendor = vendor
        self.price = price
        self.email = email


@app.route('/', methods=['GET', 'POST'])
def home():
    # Session control
    if not session.get('logged_in'):
        return render_template('index.html')
    else:

        data = []
        if 'user' and 'email' in session:
            data.append(session['user'])
            data.append(session['email'])

        # Implement loading bar here

        # myobj = Spending_History(session['email'], session['password'])
        # df = myobj.webpage_to_dataframe()

        return render_template('index.html', data=data)


@app.route('/spending_graph', methods=['GET', 'POST'])
def spending_history():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        # do stuff here with plotly

        df = stats.graphed_spending()

        graph = dict(
            data=[go.Scatter(
                x=df.index,
                y=df['currentval']
            )],
            layout=dict(
                title='Scatter Plot',
                yaxis=dict(
                    title="Spending"
                ),
                xaxis=dict(
                    title="Date"
                )
            )
        )
        graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('spending_history.html', graphJSON=graphJSON)


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
    app.debug = True
    db.create_all()
    app.run()
