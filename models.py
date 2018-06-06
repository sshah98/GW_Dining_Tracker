from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String())
    lname = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

    def __init__(self, fname, lname, email, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    account = db.Column(db.Text)
    time = db.Column(db.DateTime)
    vendor = db.Column(db.Text)
    price = db.Column(db.Float)
    email = db.Column(db.String(), db.ForeignKey('users.email'))
    datetime = db.Column(db.DateTime)

    def __init__(self, date, account, time, vendor, price, email, datetime):
        self.date = date
        self.account = account
        self.time = time
        self.vendor = vendor
        self.price = price
        self.email = email
        self.datetime = datetime

    def __repr__(self):
        return '<id {}>'.format(self.id)
