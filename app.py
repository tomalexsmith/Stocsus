from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Use your own database for testing
# Connecting to team database will be done towards the end on campus/VM
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://DB_USER:DB_PASS@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
