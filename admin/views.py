# IMPORTS
import logging
from functools import wraps

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

import database.models as database
from app import db
from users.forms import FavouriteForm, BlacklistForm


# CONFIG

# ROLES
def requires_roles(*roles):
    """
    Contains all the functionality needed to implement roles on functions
    If the logged-in user's role is not the same as the specified role.
    Adds the unauthorized attempt to the logs on the admin page.
    Redirects user to error page 403.
    """

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                logging.warning(
                    'SECURITY - Unauthorised access attempt [%s, %s, %s, %s]',
                    current_user.id,
                    current_user.email,
                    current_user.role,
                    request.remote_addr
                )
                # Redirect the user to an unauthorised notice!
                return render_template('403.html')
            return f(*args, **kwargs)

        return wrapped

    return wrapper


admin_blueprint = Blueprint('admin', __name__, template_folder = 'templates')


# view admin homepage
@admin_blueprint.route('/admin', methods = ['GET', 'POST'])
@login_required
@requires_roles('admin')
def admin():
    """
    Only users with an admin role can access this function

    Presents all registered users with ability to ban

    Presents all banned users with ability to unban

    Presents all favourite suppliers with ability to remove or add

    Presents all blacklisted suppliers with ability to remove or add

    Presents last 10 security logs
    """

    # check if the database is online
    database.database_check()

    favourite_form = FavouriteForm()
    blacklist_form = BlacklistForm()

    with open("Stocsus.log", "r") as f:
        # returns recent 10 activities
        content = f.read().splitlines()[-10:]
        content.reverse()

    if request.form.get("remove_favourite"):
        favourite_supplier = database.Favourite.query.filter_by(
            supplier_name = request.form.get("remove_favourite")
        ).first()
        if not favourite_supplier:
            flash('Supplier is not a favourite')
            return redirect(url_for('admin.admin'))

        remove_favourite_supplier = database.Favourite.query.filter_by(
            supplier_name = request.form.get("remove_favourite")
        ).first()
        db.session.delete(remove_favourite_supplier)
        db.session.commit()

    if request.form.get("remove_blacklist"):
        blacklist_supplier = database.Blacklist.query.filter_by(
            supplier_name = request.form.get("remove_blacklist")
        ).first()

        if not blacklist_supplier:
            flash('Supplier is NOT on the blacklist')
            return redirect(url_for('admin.admin'))

        remove_blacklist_supplier = database.Blacklist.query.filter_by(
            supplier_name = request.form.get("remove_blacklist")
        ).first()
        db.session.delete(remove_blacklist_supplier)
        db.session.commit()

    if request.form.get("unban"):
        user_email = database.Users.query.filter_by(email = request.form.get("unban"), banned = False).first()
        if user_email:
            flash("User is not banned")
            return redirect(url_for('admin.admin'))
        banned_user = database.Users.query.filter_by(email = request.form.get("unban")).first()
        banned_user.banned = False
        db.session.commit()
        return redirect(url_for('admin.admin'))

    if request.form.get("ban"):
        user_email = database.Users.query.filter_by(email = request.form.get("ban"), banned = True).first()
        if user_email:
            flash("User is already banned")
            return redirect(url_for('admin.admin'))
        unbanned_user = database.Users.query.filter_by(email = request.form.get("ban")).first()

        unbanned_user.banned = True
        db.session.commit()
        return redirect(url_for('admin.admin'))

    if favourite_form.validate_on_submit():
        favourite_supplier = database.Favourite.query.filter_by(
            supplier_name = favourite_form.favourite_supplier.data
        ).first()
        if favourite_supplier:
            flash('Supplier already a favourite', "favourite_alert_admin")
            return redirect(url_for('admin.admin'))

        new_favourite_supplier = database.Favourite(supplier_name = favourite_form.favourite_supplier.data)
        db.session.add(new_favourite_supplier)
        db.session.commit()

    if blacklist_form.validate_on_submit():
        blacklist_supplier = database.Blacklist.query.filter_by(
            supplier_name = blacklist_form.blacklist_supplier.data
        ).first()
        if blacklist_supplier:
            flash('Supplier already blacklisted', "blacklist_alert_admin")
            return redirect(url_for('admin.admin'))

        new_blacklist_supplier = database.Blacklist(supplier_name = blacklist_form.blacklist_supplier.data)
        db.session.add(new_blacklist_supplier)
        db.session.commit()

    return render_template('admin.html',
                           current_users = database.Users.query.filter_by(role = 'user', banned = False).all(),
                           current_banned_users = database.Users.query.filter_by(role = 'user', banned = True).all(),
                           current_favourites = database.Favourite.query.all(),
                           current_blacklist = database.Blacklist.query.all(),
                           logs = content,
                           fav_form = favourite_form,
                           blacklist_form = blacklist_form,
                           email = current_user.email
                           )
