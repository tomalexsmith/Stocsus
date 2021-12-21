# IMPORTS
from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from app import db, requires_roles
from models import User, Draw

# CONFIG
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# view admin homepage
@admin_blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def admin():
    with open("Stocsus.log", "r") as f:
        content = f.read().splitlines()[-10:]
        content.reverse()
    return render_template('admin.html', email=current_user.email,
                           current_users=User.query.filter_by(
                               role='user').all(), logs=content)

