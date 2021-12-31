# IMPORTS
import logging
from flask import Blueprint, render_template, flash, redirect, url_for, \
    request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from users.forms import RegisterForm, LoginForm
from models import Users, Favourite
from app import db
from admin.views import admin

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# VIEWS
# view registration
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = RegisterForm()

    if request.method == 'POST':
        user = Users.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the user already exists in the
        # database. Hence the user will be redirected to the signup page
        # with an error message, so the use can try again.
        if user:
            flash('Email address already exists')
            return render_template('register.html', form=form)

        # create a new user with the form data
        new_user = Users(email=form.email.data,
                         password=form.password.data,
                         role='user', banned=False)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        logging.warning('SECURITY - User registration [%s, %s]',
                        form.email.data, request.remote_addr)

        # sends the user to the login page
        return redirect(url_for('users.login'))
    # if request method is GET or form not valid re-render signup page
    return render_template('register.html', form=form)


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # if session attribute logins does not exist create attribute logins
    if not session.get('logins'):
        session['logins'] = 0
    # if login attempts is 3 or more create an error message
    elif session.get('logins') >= 3:
        flash('Number of incorrect logins exceeded')

    form = LoginForm()
    if request.method == 'POST':

        # increase login attempts by 1
        session['logins'] += 1

        user = Users.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(user.password, form.password.data):

            # if no match create appropriate error message based on login attempts
            if session['logins'] == 3:
                flash('Number of incorrect logins exceeded')
                logging.warning('SECURITY - Invalid login attempt [%s, %s]', form.email.data, request.remote_addr)
            elif session['logins'] == 2:
                flash('Please check your login details and try again. 1 login attempt remaining')
                logging.warning('SECURITY - Invalid login attempt [%s, %s]', form.email.data, request.remote_addr)
            else:
                flash('Please check your login details and try again. 2 login attempts remaining')
                logging.warning('SECURITY - Invalid login attempt [%s, %s]', form.email.data, request.remote_addr)

            return render_template('login.html', form=form)

        if user and check_password_hash(user.password, form.password.data):

            # if user is verified reset login attempts to 0
            session['logins'] = 0

            login_user(user)

            db.session.add(user)
            db.session.commit()

            logging.warning('SECURITY - Log in [%s, %s, %s]', current_user.id, current_user.email,
                            request.remote_addr)

            if current_user.role == 'admin':
                return admin()
            else:
                return redirect(url_for('search_blueprint.search'))
        else:
            logging.warning('SECURITY - Invalid login attempt [%s, %s]', form.email.data, request.remote_addr)

    return render_template('login.html', form=form)


@users_blueprint.route('/dashboard')
@login_required
def dashboard():
    submitted_favourite = ''
    submitted_favourite = request.form.get('favourite')
    submitted_favourite.strip()

    new_favourite = Favourite(supplier_name=submitted_favourite)

    db.session.add(new_favourite)
    db.session.commit()

    flash('Favourite added.')
    return render_template('dashboard.html', email=current_user.email,
                           favourites=Favourite)


@users_blueprint.route('/logout')
@login_required
def logout():
    logging.warning('SECURITY - Log out [%s, %s, %s]', current_user.id,
                    current_user.username, request.remote_addr)

    logout_user()
    return redirect(url_for('index'))


def favourites(supplier_name):
    # TODO - to use in the future to select favourite supplier
    query = "INSERT INTO favourite(supplier_name)"
    args = supplier_name

    db.session.add(supplier_name)
    db.session.commit()


def blacklist(supplier_name):
    # TODO - to use when adding a supplier to the blacklist
    query = "INSERT INTO blacklist(supplier_name)"
    args = supplier_name

    db.session.add(supplier_name)
    db.session.commit()
