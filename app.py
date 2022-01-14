# IMPORTS
import logging
from functools import wraps
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import os


db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    # SECRET KEYS
    app.config['SECRET_KEY'] = os.urandom(32)
    app.config['WTF_CSRF_SECRET_KEY'] = os.urandom(32)
    app.config[
            'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@stocsus.cl2ccsjbwdx3.us-east-1.rds.amazonaws.com:3306/stocsus'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    #from database.models import Users

    # BLUEPRINTS

    # importing blueprints
    from users.views import users_blueprint
    from admin.views import admin_blueprint
    from search.views import search_blueprint

    # registering blueprints
    app.register_blueprint(users_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(search_blueprint)

    # Home Page
    @app.route('/')
    def index():  # put application's code here
        print(request.headers)
        return render_template('index.html')

    # ERROR PAGE VIEWS
    # TODO - Create templates for the error pages
    @app.errorhandler(400)
    def bad_request(error):
        return render_template('400.html'), 400

    @app.errorhandler(403)
    def page_forbidden(error):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    @app.errorhandler(503)
    def service_unavailable(error):
        return render_template('503.html'), 503

    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)




@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

