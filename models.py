from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash


# Database table containing user information
# email and password are what the user enters when they register
# role defines which parts of the application the user has access to
# banned is False by default which is stored as 0 in the database, False = 0 / True = 1
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(64), nullable=False, default='user')
    banned = db.Column(db.BOOLEAN, nullable=False, default=False)

    def __init__(self, email, password, role, banned):
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.banned = banned


# Database table containing name of suppliers that have been blacklisted by users
class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(64), nullable=False)

    def __init__(self, supplier_name):
        self.supplier_name = supplier_name


# Database table containing the name of suppliers that have been favourited by users
class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(64), nullable=False)

    def __init__(self, supplier_name):
        self.supplier_name = supplier_name


db.create_all()


# initialises database tables and adds sample data
# Python Console --> from model import init_db
#                --> init_db()
def init_db():
    db.drop_all()
    db.create_all()
    test = Users(email="test", password="test123", role="admin", banned=False)
    fav = Favourite(supplier_name="my-favourite")
    black = Blacklist(supplier_name="the-worst")
    db.session.add(test)
    db.session.add(fav)
    db.session.add(black)
    db.session.commit()
