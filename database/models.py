import sqlalchemy
from sqlalchemy import exc
from flask_login import UserMixin
from flask import request, render_template
from app import db
from werkzeug.security import generate_password_hash


# Table containing user information
class Users(db.Model, UserMixin):
    __table_name__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # email and password are what the user enters when they register
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    # role defines which parts of the application the user has access to
    role = db.Column(db.String(64), nullable=False, default='user')
    # banned is False by default which is stored as 0 in the database,
    # False = 0 / True = 1
    banned = db.Column(db.BOOLEAN, nullable=False, default=False)

    def __init__(self, email, password, role, banned):
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.banned = banned


# Table containing name of suppliers that have been blacklisted by users
class Blacklist(db.Model):
    __table_name__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(64), nullable=False, unique=True)

    def __init__(self, supplier_name):
        self.supplier_name = supplier_name


# Table containing the name of suppliers that have been
# made a favourite by users
class Favourite(db.Model):
    __table_name__ = 'favourites'

    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(64), nullable=False, unique=True)

    def __init__(self, supplier_name):
        self.supplier_name = supplier_name

# Table containing all the part numbers that user want to watch
class WatchList(db.Model):
    __table_name__ = 'watchlist'

    id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String(64), nullable=False, unique=True)

    def __init__(self, part_number):
        self.part_number = part_number


def database_check():
    """
    if the database is offline then to prevent the application crashing
    error is caught by doing a test query on the database.
    Predefined error message is displayed.
    """
    try:
        Favourite.query.filter_by(
            supplier_name=request.form.get("Test")).first()
    except sqlalchemy.exc.OperationalError as database_error:
        if database_error.orig.args[0] == 1045:
            # 1045 is access denied error
            return render_template("database_error.html",
                                   message="Error 1045 connecting to application, please contact IT support")

        elif database_error.orig.args[0] == 2003:
            # 2003 is a connection error with the database
            return render_template("database_error.html",
                                   message="Error 2003 connecting to application, please contact IT support")







def init_db():
    """
    initialises database tables and adds sample data
    Python Console --> from database.models import init_db
                    --> init_db()
    """
    db.drop_all()
    db.create_all()
    test = Users(email="test@email.com", password="@Test123", role="admin",
                 banned=False)
    fav = Favourite(supplier_name="my-favourite")
    black = Blacklist(supplier_name="the-worst")
    db.session.add(test)
    db.session.add(fav)
    db.session.add(black)
    db.session.commit()
