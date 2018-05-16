from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from spending import Spending_History


APPNAME = 'GWorld Spending'

app = Flask(__name__)
app.config.update(APPNAME=APPNAME,)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = "123"

db = SQLAlchemy(app)

# myobj = Spending_History('suraj98@gwu.edu', 'Nebulae101!')
# data = myobj.webpage_to_dataframe()
# print(data)


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


@app.route('/', methods=['GET', 'POST'])
def home():
    # Session control
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            # username = getname(request.form['username'])
            # return render_template('index.html')
            # origina instgram thing -- this is where the gw app comes into play
            myobj = Spending_History(self.email, self.password)
            data = myobj.webpage_to_dataframe()
            print(data)

            
            return render_template('index.html', data=data)
        else:
            return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # login form
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # _user = request.form['username']
        _email = request.form['email']
        _pass = request.form['password']
        try:
            data = User.query.filter_by(email=_email, password=_pass).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return render_template("404.html")
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

            return render_template('login.html')
    except exc.IntegrityError:
        return render_template("404.html")

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
