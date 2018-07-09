# -*- coding: utf-8 -*-
import json
import sys
import os
import hashlib
import plotly
import psycopg2
import datetime
import pandas as pd
import numpy as np
import plotly.graph_objs as go

from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, cross_validation, svm

from flask import Flask, redirect, url_for, render_template, request, session, flash, Markup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_socketio import SocketIO, emit

from spending import SpendingHistory

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio = SocketIO(app)
database = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='allow')

db = SQLAlchemy(app)

from models import *

# ======== Routing =========================================================== #


@app.route('/', methods=['GET', 'POST'])
def home():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:

        df = pd.read_sql_query(
            "SELECT * FROM history WHERE email='%s'" % (session['email']), database)
    try:
        if df.empty:
            flash(Markup(
                "<p><b>Please click <a href='/refresh'>refresh now</a> to get the latest data!</b></p>"))
    
            
        else:

            data = User.query.filter_by(email=session['email']).first()
            predicted_days = 7

            if data.kitchen == "yes":
                initial_gworld = 1400

            elif data.kitchen == "no":
                initial_gworld = 2600
            else:
                initial_gworld = 1350

            df['currentval'] = np.nan
            df['currentval'] = df['price'] - df['currentval']
            df.currentval = initial_gworld + df.price.cumsum()
            df.drop(columns=['date', 'time'], inplace=True)
            df.set_index('datetime', inplace=True)

            df = df[['currentval']]

            forecast_out = int(7)  # predicting 30 days into future
            # label column with data shifted 30 units up
            df['Prediction'] = df[['currentval']].shift(-forecast_out)

            X = np.array(df.drop(['Prediction'], 1))
            X = preprocessing.scale(X)

            X_forecast = X[-forecast_out:]  # set X_forecast equal to last 30
            X = X[:-forecast_out]  # remove last 30 from X
            y = np.array(df['Prediction'])
            y = y[:-forecast_out]
            X_train, X_test, y_train, y_test = cross_validation.train_test_split(
                X, y, test_size=0.2)

            clf = LinearRegression()
            clf.fit(X_train, y_train)

            confidence = clf.score(X_test, y_test)  # Testing
            forecast_prediction = clf.predict(X_forecast)

            future_days_list = []
            for i in range(1, predicted_days + 1):
                future_days_list.append(
                    df.tail(1).index + datetime.timedelta(days=i))

            predicted_df = pd.DataFrame(future_days_list)
            forecast = pd.Series(forecast_prediction)
            predicted_df['currentval'] = forecast.values
            predicted_df.columns = ['datetime', 'price']
            predicted_df['datetime'] = predicted_df['datetime'].dt.date
            predicted_df.set_index('datetime', inplace=True)

            graph = dict(
                data=[go.Scatter(
                    x=predicted_df.index,
                    y=predicted_df['price']
                )],
                layout=dict(
                    title='Predicted Week of Spending',
                    hovermode='closest',
                    yaxis=dict(
                        title="Price"
                    ),
                    xaxis=dict(
                        title="Days"
                    )
                )
            )
            graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('home.html', user=session['name'], graphJSON=graphJSON, predicted_df=predicted_df)

    except UnboundLocalError as e:
        
        return render_template('home.html', user=session['name'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    # login form
    if request.method == 'GET':
        return render_template('login.html')
    else:
        _email = request.form['email']
        _pass = hashlib.md5(request.form['pass'].encode())
        _pass = _pass.hexdigest()

        try:

            # hash the password. if the same, then login
            data = User.query.filter_by(email=_email, password=_pass).first()

            if data is not None:
                session['logged_in'] = True
                session['email'] = request.form['email']
                session['pass'] = request.form['pass']
                session['name'] = session['email'].split("@")[0]

                return redirect(url_for('home'))
            else:
                flash(Markup("<p><center>Wrong Email/Password!</center></p>"))
                return render_template('login.html')
        except:
            flash(Markup(
                "<p><center>Sorry there has been an error! Please Try Again.</center></p>"))
            return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def register():
    # registration form
    if request.method == 'GET':
        return render_template('signup.html')

    try:
        if request.method == 'POST':

            password = hashlib.md5(request.form['pass'].encode())
            hashed_pass = password.hexdigest()

            kitchen_response = request.form['demo-priority']

            new_user = User(
                name=request.form['name'], email=request.form['email'], password=hashed_pass, kitchen=kitchen_response)

            db.session.add(new_user)
            db.session.commit()

            session['email'] = request.form['email']
            session['pass'] = request.form['pass']
            session['name'] = session['email'].split("@")[0]

            flash(Markup("<p><center>Please login now!</center></p>"))
            return render_template('login.html')

    except exc.IntegrityError:
        flash(Markup(
            "<p><center>Sorry there has been an error! Please Try Again.</center></p>"))
        return render_template("signup.html")


@app.route('/info', methods=['GET', 'POST'])
def info():
    if session.get('logged_in'):
        return render_template('info.html', user=session['name'])
    else:
        return redirect(url_for('login'))


@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    if session.get('logged_in'):
        try:
            SpendingHistory(session['email'],
                            session['pass']).spending_history()
            flash(Markup("<p><b>GWorld Dining Dollars Updated!</b></p>"))

        except ConnectionError as e:
            flash(
                Markup("<p><b>Unable to connect to GET. Please try again later!</b></p>"))

        finally:
            return redirect(url_for('home'))

    else:
        return redirect(url_for('login'))


@app.route('/map', methods=['GET', 'POST'])
def map():
    if session.get('logged_in'):
        return render_template('map.html')
    else:
        return redirect(url_for('login'))


@app.route('/spending_graph', methods=['GET', 'POST'])
def spending_history():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:

        initial_gworld = 1350

        df = pd.read_sql_query(
            "SELECT * FROM history WHERE email='%s'" % (session['email']), database)
        df['currentval'] = np.nan
        df['currentval'] = df['price'] - df['currentval']
        df.currentval = initial_gworld + df.price.cumsum()
        df.drop(columns=['date', 'time'], inplace=True)
        df.set_index('datetime', inplace=True)

        graph = dict(
            data=[go.Scatter(
                x=df.index,
                y=df['currentval']
            )],
            layout=dict(
                title='Total Spending By Day',
                yaxis=dict(
                    title="Spending"
                ),
                xaxis=dict(
                    title="Date"
                )
            )
        )
        graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
        # graphJSON = Markup(graphJSON)

        return render_template('spending_graph.html', graphJSON=graphJSON)


# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        if request.method == "POST":
            if request.form['pass'] != "":
                password = hashlib.md5(request.form['pass'].encode())
                hashed_pass = password.hexdigest()

                user = User.query.filter_by(email=session['email']).first()
                user.password = hashed_pass

                kitchen_response = request.form['demo-priority']
                user.kitchen = kitchen_response
                db.session.commit()

            elif request.form['pass'] == "":
                user = User.query.filter_by(email=session['email']).first()

                kitchen_response = request.form['demo-priority']
                user.kitchen = kitchen_response
                db.session.commit()

            flash(Markup("<p><center>User Information Updated!</center></p>"))

        return render_template('settings.html', user=session['email'])


# -------- Logout ---------------------------------------------------------- #
@app.route('/logout/')
def logout():
    # logout form
    session['logged_in'] = False
    flash(Markup("<p><center>You have logged out. Thank you!</center></p>"))
    return redirect(url_for('home'))


@socketio.on('disconnect')
def disconnect_user():
    session.clear()
    session.pop('random-key', None)



# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
