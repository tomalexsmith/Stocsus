# IMPORTS
from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from app import db, requires_roles
from models import Users

# CONFIG
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# view admin homepage
@admin_blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def admin():
    with open("Stocsus.log", "r") as f:
        # returns recent 10 activities
        content = f.read().splitlines()[-10:]
        content.reverse()
    # returns the email of the current user
    # returns list of all users in the database where their role is a 'user'
    # returns the security logs
    return render_template('admin.html', email=current_user.email,
                           current_users=Users.query.filter_by(
                               role='user').all(), logs=content)

