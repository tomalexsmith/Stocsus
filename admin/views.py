# IMPORTS
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
import app
import database.models as database
import admin.forms as admin_form
import users.forms as user_form

# CONFIG
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# view admin homepage
@admin_blueprint.route('/admin', methods=['GET', 'POST'])
# @login_required
# @requires_roles('admin')
def admin():
    ban_form = admin_form.BanForm()
    unban_form = admin_form.UnbanForm()
    remove_favourite_form = user_form.FavouriteForm()
    remove_blacklist_form = user_form.BlacklistForm()

    with open("Stocsus.log", "r") as f:
        # returns recent 10 activities
        content = f.read().splitlines()[-10:]
        content.reverse()

    if remove_favourite_form.validate_on_submit():
        favourite_supplier = database.Favourite.query.filter_by(
            supplier_name=remove_favourite_form.favourite_supplier.data).first()
        if not favourite_supplier:
            flash('Supplier is not a favourite')
            return redirect(url_for('admin.admin'))

        remove_favourite_supplier = database.Favourite.query.filter_by(
            supplier_name=remove_favourite_form.favourite_supplier.data).first()
        app.db.session.delete(remove_favourite_supplier)
        app.db.session.commit()

    if remove_blacklist_form.validate_on_submit():
        blacklist_supplier = database.Blacklist.query.filter_by(
            supplier_name=remove_blacklist_form.blacklist_supplier.data).first()

        if not blacklist_supplier:
            flash('Supplier is NOT on the blacklist')
            return redirect(url_for('admin.admin'))

        remove_blacklist_supplier = database.Blacklist.query.filter_by(
            supplier_name=remove_blacklist_form.blacklist_supplier.data).first()
        app.db.session.delete(remove_blacklist_supplier)
        app.db.session.commit()

    if unban_form.validate_on_submit():
        user_email = database.Users.query.filter_by(email=unban_form.email_to_unban.data, banned=False).first()
        if user_email:
            flash("User is not banned")
            return redirect(url_for('admin.admin'))
        banned_user = database.Users.query.filter_by(email=unban_form.email_to_unban.data).first()
        banned_user.banned = False
        app.db.session.commit()
        return redirect(url_for('admin.admin'))
    if ban_form.validate_on_submit():
        user_email = database.Users.query.filter_by(email=ban_form.email_to_ban.data, banned=True).first()
        if user_email:
            flash("User is already banned")
            return redirect(url_for('admin.admin'))
        unbanned_user = database.Users.query.filter_by(email=ban_form.email_to_ban.data).first()

        unbanned_user.banned = True
        app.db.session.commit()
        return redirect(url_for('admin.admin'))

    return render_template('admin.html',
                           current_users=database.Users.query.filter_by(role='user', banned=False).all(),
                           current_banned_users=database.Users.query.filter_by(role='user', banned=True).all(),
                           current_favourites=database.Favourite.query.all(),
                           current_blacklist=database.Blacklist.query.all(),
                           logs=content,
                           ban_form=ban_form,
                           unban_form=unban_form,
                           remove_favourite_form=remove_favourite_form,
                           remove_blacklist_form=remove_blacklist_form
                           )
    # To add after testing: email=current_username.email

