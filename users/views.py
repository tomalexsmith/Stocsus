# IMPORTS
import logging

from flask import Blueprint, render_template, flash, redirect, url_for, \
    request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash

import app
import database.models as database
from users.forms import RegisterForm, LoginForm, FavouriteForm, BlacklistForm


# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder = 'templates')


# VIEWS
# view registration
@users_blueprint.route('/register', methods = ['GET', 'POST'])
def register():
    database.database_check()
    # create signup form object
    form = RegisterForm()

    if form.validate_on_submit():
        database.database_check()
        user = database.Users.query.filter_by(email = form.email.data).first()
        # if this returns a user, then the user already exists in the
        # database. Hence the user will be redirected to the signup page
        # with an error message, so the use can try again.
        if user:
            flash('Email address already exists')
            return render_template('register.html', form = form)

        # create a new user with the form data
        new_user = database.Users(email = form.email.data,
                                  password = form.password.data,
                                  role = 'user', banned = False
                                  )

        # add the new user to the database
        app.db.session.add(new_user)
        app.db.session.commit()

        logging.warning('SECURITY - User registration [%s, %s]',
                        form.email.data, request.remote_addr
                        )
        # login the registered user
        new_user = database.Users.query.filter_by(email = form.email.data).first()
        login_user(new_user)
        # sends the user to the search page
        return redirect(url_for('search_blueprint.search'))
    # if request method is GET or form not valid re-render signup page
    return render_template('register.html', form = form)


# view user login
@users_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
    database.database_check()
    user_is_banned = False
    # if session attribute logins does not exist create attribute logins
    if not session.get('logins'):
        session['logins'] = 0
    # if login attempts is 3 or more create an error message
    elif session.get('logins') >= 3:
        flash('Number of incorrect logins exceeded')

    form = LoginForm()
    if form.validate_on_submit():
        database.database_check()
        user = database.Users.query.filter_by(email = form.email.data).first()
        if user and not database.Users.query.filter_by(email = form.email.data, banned = False).first():
            flash("Access denied, please contact an administrator")
            return render_template('login.html', form = form)

        # increase login attempts by 1
        session['logins'] += 1

        user = database.Users.query.filter_by(email = form.email.data).first()

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

            return render_template('login.html', form = form)

        if user and check_password_hash(user.password, form.password.data):

            # if user is verified reset login attempts to 0
            session['logins'] = 0

            login_user(user)

            app.db.session.add(user)
            app.db.session.commit()

            logging.warning('SECURITY - Log in [%s, %s, %s]', current_user.id, current_user.email,
                            request.remote_addr
                            )

            if current_user.role == 'admin':
                return redirect((url_for('admin.admin')))
            else:
                return redirect(url_for('search_blueprint.search'))
        else:
            logging.warning('SECURITY - Invalid login attempt [%s, %s]', form.email.data, request.remote_addr)

    return render_template('login.html', form = form)


@users_blueprint.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
    """
    Shows users all favourite and blacklisted suppliers with ability to add.
    Shows users all part numbers that have been added to the watchlist with ability to add or remove
    """
    # checks if database is online
    database.database_check()

    favourite_form = FavouriteForm()
    blacklist_form = BlacklistForm()

    if favourite_form.validate_on_submit():
        favourite_supplier = database.Favourite.query.filter_by(
            supplier_name = favourite_form.favourite_supplier.data
        ).first()
        if favourite_supplier:
            flash('Supplier already a favourite', "favourite_alert")
            return redirect(url_for('users.dashboard'))

        new_favourite_supplier = database.Favourite(supplier_name = favourite_form.favourite_supplier.data)
        app.db.session.add(new_favourite_supplier)
        app.db.session.commit()

    if blacklist_form.validate_on_submit():
        blacklist_supplier = database.Blacklist.query.filter_by(
            supplier_name = blacklist_form.blacklist_supplier.data
        ).first()
        if blacklist_supplier:
            flash('Supplier already blacklisted', "blacklist_alert")
            return redirect(url_for('users.dashboard'))

        new_blacklist_supplier = database.Blacklist(supplier_name = blacklist_form.blacklist_supplier.data)
        app.db.session.add(new_blacklist_supplier)
        app.db.session.commit()

    if request.form.get("remove_watchlist"):
        remove_watchlist_supplier = database.WatchList.query.filter_by(
            part_number = request.form.get("remove_watchlist")
        ).first()
        app.db.session.delete(remove_watchlist_supplier)
        app.db.session.commit()
        return redirect(url_for('users.dashboard'))

    return render_template('dashboard.html', current_favourites = database.Favourite.query.all(),
                           current_blacklist = database.Blacklist.query.all(), favourite_form = favourite_form,
                           blacklist_form = blacklist_form, watchlist = database.WatchList.query.all(),
                           email = current_user.email, role = current_user.role
                           )


@users_blueprint.route('/logout')
@login_required
def logout():
    """
    Should only be visible if user is logged in
    Logs the details of the user that logged out
    """

    logging.warning('SECURITY - Log out [%s, %s, %s]', current_user.id,
                    current_user.email, request.remote_addr
                    )

    logout_user()
    return redirect(url_for('index'))
