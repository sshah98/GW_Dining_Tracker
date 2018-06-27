# -*- coding: utf-8 -*-
import json
import sys
import os
import plotly
import pandas as pd
import numpy as np
import plotly.graph_objs as go


from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session, flash, Markup
from flask_socketio import SocketIO, emit

from stats import graphed_spending
from spending import Spending_History

app = Flask(__name__)
socketio = SocketIO(app)
 

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


@app.route('/refresh', methods=['GET', 'POST'])
def refresh():

    myobj = Spending_History(session['email'], session['password'])
    df = myobj.webpage_to_dataframe()

    flash('GWorld Dining Dollars Data Updated!')

    return render_template('home.html')


# @app.route('/spending_graph', methods=['GET', 'POST'])
# def spending_history():
#     if not session.get('logged_in'):
#         form = forms.LoginForm(request.form)
#     else:
#         df = graphed_spending()
#         graph = dict(
#             data=[go.Scatter(
#                 x=df.index,
#                 y=df['currentval']
#             )],
#             layout=dict(
#                 title='Scatter Plot',
#                 yaxis=dict(
#                     title="Spending"
#                 ),
#                 xaxis=dict(
#                     title="Date"
#                 )
#             )
#         )
#         graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
#         graphJSON = Markup(graphJSON)
#
#         return render_template('spending_history.html', graphJSON=graphJSON)


@socketio.on('disconnect')
def disconnect_user():
    session.clear()
    session.pop('random-key', None)


# ======== Main ============================================================== #
if __name__ == "__main__":
    app.secret_key = os.urandom(12)  # Generic key for dev purposes only
    app.run(debug=True, use_reloader=True)
