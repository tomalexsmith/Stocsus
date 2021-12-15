# IMPORTS
from flask import Blueprint, render_template, flash, redirect, url_for, \
    request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from users.forms import register_form, login_form
from models import Users
from app import db

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# VIEWS
# view registration
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = register_form()

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

        # sends the user to the login page
        return redirect(url_for('users.login'))
    # if request method is GET or form not valid re-render signup page
    return render_template('register.html', form=form)


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get('logins'):
        session['logins'] = 0
    elif session.get('logins') >= 3:
        flash('Number of incorrect logins exceeded')

    form = login_form()

    if form.validate_on_submit():
        session['logins'] += 1
        user = Users.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(user.password,
                                               form.password.data):
            if session['logins'] == 3:
                flash('Number of incorrect logins exceeded')
            elif session['logins'] == 2:
                flash(
                    'Please check your login details and try again. 1 login attempt remaining')
            else:
                flash(
                    'Please check your login details and try again. 2 login attempts remaining')
            return render_template('login.html', form=form)

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
    logout_user()
    return redirect(url_for('home'))

def favourites(supplier_name):
    query = "INSERT INTO favourite(supplier_name)"
    args = supplier_name

    db.session.add(supplier_name)
    db.session.commit()

