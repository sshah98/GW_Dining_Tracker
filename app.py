# -*- coding: utf-8 -*-
import json
import sys
import os
import plotly
import psycopg2
import pandas as pd
import numpy as np
import plotly.graph_objs as go


from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session, flash, Markup
from flask_socketio import SocketIO, emit

from spending import SpendingHistory

app = Flask(__name__)
app.secret_key = 'random-key'  # Generic key for dev purposes only

socketio = SocketIO(app)
DATABASE_URL = os.environ['DATABASE_URL']
database = psycopg2.connect(DATABASE_URL, sslmode='allow')


# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    session['password'] = request.form['password']
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = helpers.get_user()
    session['email'] = user.email
    return render_template('home.html', user=user)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = helpers.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if not helpers.username_taken(username):
                    helpers.add_user(username, password, email)
                    session['logged_in'] = True
                    session['username'] = username
                    session['email'] = request.form['email']
                    session['password'] = request.form['password']
                    return json.dumps({'status': 'Signup successful'})
                return json.dumps({'status': 'Username taken'})
            return json.dumps({'status': 'User/Pass required'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))


# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))


@app.route('/info', methods=['GET', 'POST'])
def info():
    if session.get('logged_in'):
        return render_template('info.html', user=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/refresh', methods=['GET', 'POST'])
def refresh():

    SpendingHistory(session['email'], session['password']).spending_history()
    # print(session['spending'])

    flash('GWorld Dining Dollars Data Updated!')

    return render_template('home.html')


@app.route('/spending_graph', methods=['GET', 'POST'])
def spending_history():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
    else:
 
        initial_gworld = 1350

        df = pd.read_sql_query("SELECT * FROM history WHERE email='%s'" %(session['email']), database)
        df['currentval'] = np.nan
        df['currentval'] = df['price'] - df['currentval']
        df.currentval = initial_gworld + df.price.cumsum()
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

        return render_template('spending_history.html', graphJSON=graphJSON)


@socketio.on('disconnect')
def disconnect_user():
    session.clear()
    session.pop('random-key', None)


# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
