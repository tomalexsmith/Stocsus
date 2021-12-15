from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Use your own database for testing
# Connecting to team database will be done towards the end on campus/VM
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@stocsus.cs4jpvtwcnto.eu-west-2.rds.amazonaws.com:3306/stocsus'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
