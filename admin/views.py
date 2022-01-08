# IMPORTS
import sqlalchemy
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import exc

import app
import database.models as database
from users.forms import FavouriteForm, BlacklistForm

# CONFIG


admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# view admin homepage
@admin_blueprint.route('/admin', methods=['GET', 'POST'])
# @login_required
# @requires_roles('admin')
def admin():
    database.database_check()

    favourite_form = FavouriteForm()
    blacklist_form = BlacklistForm()

    with open("Stocsus.log", "r") as f:
        # returns recent 10 activities
        content = f.read().splitlines()[-10:]
        content.reverse()

    if request.form.get("remove_favourite"):
        favourite_supplier = database.Favourite.query.filter_by(
            supplier_name=request.form.get("remove_favourite")).first()
        if not favourite_supplier:
            flash('Supplier is not a favourite')
            return redirect(url_for('admin.admin'))

        remove_favourite_supplier = database.Favourite.query.filter_by(
            supplier_name=request.form.get("remove_favourite")).first()
        app.db.session.delete(remove_favourite_supplier)
        app.db.session.commit()

    if request.form.get("remove_blacklist"):
        blacklist_supplier = database.Blacklist.query.filter_by(
            supplier_name=request.form.get("remove_blacklist")).first()

        if not blacklist_supplier:
            flash('Supplier is NOT on the blacklist')
            return redirect(url_for('admin.admin'))

        remove_blacklist_supplier = database.Blacklist.query.filter_by(
            supplier_name=request.form.get("remove_blacklist")).first()
        app.db.session.delete(remove_blacklist_supplier)
        app.db.session.commit()

    if request.form.get("unban"):
        user_email = database.Users.query.filter_by(email=request.form.get("unban"), banned=False).first()
        if user_email:
            flash("User is not banned")
            return redirect(url_for('admin.admin'))
        banned_user = database.Users.query.filter_by(email=request.form.get("unban")).first()
        banned_user.banned = False
        app.db.session.commit()
        return redirect(url_for('admin.admin'))

    if request.form.get("ban"):
        user_email = database.Users.query.filter_by(email=request.form.get("ban"), banned=True).first()
        if user_email:
            flash("User is already banned")
            return redirect(url_for('admin.admin'))
        unbanned_user = database.Users.query.filter_by(email=request.form.get("ban")).first()

        unbanned_user.banned = True
        app.db.session.commit()
        return redirect(url_for('admin.admin'))

    if favourite_form.validate_on_submit():
        favourite_supplier = database.Favourite.query.filter_by(
            supplier_name=favourite_form.favourite_supplier.data).first()
        if favourite_supplier:
            flash('Supplier already a favourite', "favourite_alert_admin")
            return redirect(url_for('admin.admin'))

        new_favourite_supplier = database.Favourite(supplier_name=favourite_form.favourite_supplier.data)
        app.db.session.add(new_favourite_supplier)
        app.db.session.commit()

    if blacklist_form.validate_on_submit():
        blacklist_supplier = database.Blacklist.query.filter_by(
            supplier_name=blacklist_form.blacklist_supplier.data).first()
        if blacklist_supplier:
            flash('Supplier already blacklisted', "blacklist_alert_admin")
            return redirect(url_for('admin.admin'))

        new_blacklist_supplier = database.Blacklist(supplier_name=blacklist_form.blacklist_supplier.data)
        app.db.session.add(new_blacklist_supplier)
        app.db.session.commit()

    return render_template('admin.html',
                           current_users=database.Users.query.filter_by(role='user', banned=False).all(),
                           current_banned_users=database.Users.query.filter_by(role='user', banned=True).all(),
                           current_favourites=database.Favourite.query.all(),
                           current_blacklist=database.Blacklist.query.all(),
                           logs=content,
                           fav_form=favourite_form,
                           blacklist_form=blacklist_form
                           )

    # To add after testing: email=current_username.email
