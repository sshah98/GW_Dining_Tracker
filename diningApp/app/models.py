from flask_login import UserMixin
from app import db, login
from flask_login import UserMixin



# create the columns in the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    # how to print objects
    def __repr__(self):
        return '<User {}>'.format(self.username)
        
@login.user_loader
def load_user(id):
    return User.query.get(int(id))