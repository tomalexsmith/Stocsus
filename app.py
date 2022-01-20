# IMPORTS
import logging
import os

import sqlalchemy
from flask import Flask, render_template, request, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


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
        try:
            from database.models import Users
            return Users.query.get(int(id))
        except sqlalchemy.exc.OperationalError:
            match request.path:
                case url_for('index'):
                    return render_template('index.html')
                case url_for('users.login'):
                    return render_template('login.html')
                case url_for('users.register'):
                    return render_template('register.html')
                case url_for('search_blueprint.results'):
                    return render_template('results.html')
                case url_for('admin.admin'):
                    return render_template('admin.html')
                case url_for('users.dashboard'):
                    return render_template('dashboard.html')
                case url_for('search_blueprint.search'):
                    return render_template('search.html')
    return app


# LOGGING
class SecurityFilter(logging.Filter):
    def filter(self, record):
        return "SECURITY" in record.getMessage()


fh = logging.FileHandler('Stocsus.log', 'w')
fh.setLevel(logging.WARNING)
fh.addFilter(SecurityFilter())
formatter = logging.Formatter('%(asctime)s : %(message)s',
                              '%m/%d/%Y %I:%M:%S %p'
                              )
fh.setFormatter(formatter)

logger = logging.getLogger('')
logger.propagate = False
logger.addHandler(fh)

if __name__ == '__main__':
    app = create_app()
    app.run(debug = True)
