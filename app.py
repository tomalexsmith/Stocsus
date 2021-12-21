from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os



app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)
app.config['WTF_CSRF_SECRET_KEY'] = os.urandom(32)

# Use your own database for testing
# Connecting to team database will be done towards the end on campus/VM
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://DB_USER:DB_PASS@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# BLUEPRINTS
from search import search_blueprint
app.register_blueprint(search_blueprint)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)

