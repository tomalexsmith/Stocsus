# IMPORTS
import logging
from flask import Blueprint, render_template, flash, redirect, url_for, \
    request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from users.forms import RegisterForm, LoginForm
from models import Users
from app import db

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# VIEWS
# view registration
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = RegisterForm()

    if form.validate_on_submit():
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
                         role='user')

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

    if form.validate_on_submit():
        # increase login attempts by 1
        session['logins'] += 1
        # when POST is received database is queried for
        # first username that matches
        user = Users.query.filter_by(email=form.email.data).first()

        # checks whether passwords match and if either that doesn't match
        # or username isn't found
        # asks user to check login details
        if not user or not check_password_hash(user.password,
                                               form.password.data):
            # logging call to indicate an invalid login attempt
            logging.warning('SECURITY - Invalid Login [%s]',
                            request.remote_addr)

            # if no match create appropriate error message based on
            # login attempts
            if session['logins'] == 3:
                flash('Number of incorrect logins exceeded')
            elif session['logins'] == 2:
                flash(
                    'Please check your login details and try again. 1 login '
                    'attempt remaining')
            else:
                flash(
                    'Please check your login details and try again. 2 login '
                    'attempts remaining')
            return render_template('login.html', form=form)

        login_user(user)

        # datetime doesn't work so it's commented out
        user.last_logged_in = user.current_logged_in
        # user.current_logged_in = datetime.now()
        db.session.add(user)
        db.session.commit()

        # logging call to indicate user has logged in
        logging.warning('SECURITY - Log in [%s, %s, %s]', current_user.id,
                        current_user.email,
                        request.remote_addr)

        if current_user.role == 'admin':
            return redirect(url_for('admin.admin'))
        else:
            return redirect(url_for('users.search'))

    return render_template('login.html', form=form)


@users_blueprint.route('/profile')
@login_required
def profile():
    return render_template('profile.html', email=current_user.email)


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