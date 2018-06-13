import os
import json
import plotly
import hashlib
import pandas as pd
import numpy as np
import plotly.graph_objs as go

from flask import Flask, url_for, render_template, request, redirect, session, Markup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from stats import graphed_spending
from spending import Spending_History


APPNAME = 'GWorld Spending'

app = Flask(__name__)

app.config.update(APPNAME=APPNAME,)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object('config')
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

        # TODO: Implement a loading bar in html page
        
        # myobj = Spending_History(session['email'], session['password'])
        df = myobj.webpage_to_dataframe()

        return render_template('index.html', user=name)


@app.route('/spending_graph', methods=['GET', 'POST'])
def spending_history():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        df = graphed_spending()
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
        graphJSON = Markup(graphJSON)

        return render_template('spending_history.html', graphJSON=graphJSON)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # login form
    if request.method == 'GET':
        return render_template('login.html')
    else:
        _email = request.form['email']
        _pass = hashlib.md5(request.form['password'].encode())
        _pass = _pass.hexdigest()

        try:

            # hash the password. if the same, then login
            data = User.query.filter_by(email=_email, password=_pass).first()
            if data is not None:
                session['logged_in'] = True
                session['email'] = request.form['email']
                session['password'] = request.form['password']
                session['spending'] = Spending_History(session['email'], session['password']).webpage_to_dataframe().to_json()

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

            password = hashlib.md5(request.form['password'].encode())
            password = password.hexdigest()
            new_user = User(fname=request.form['fname'], lname=request.form['lname'],
                            email=request.form['email'], password=password)

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
