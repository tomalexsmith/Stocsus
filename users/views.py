# IMPORTS
from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from users.forms import register_form, login_form
from models import Users
from app import db

#CONFIG
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
            flash('Emai; address already exists')
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
    form = login_form()