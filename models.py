from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    kitchen = db.Column(db.String())

    def __repr__(self):
        return 'Email {}>'.format(self.email)


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

    def __repr__(self):
        return '<id {}>'.format(self.id)
