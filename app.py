import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# LOGGING
class SecurityFilter(logging.Filter):
    def filter(self, record):
        return "SECURITY" in record.getMessage()


fh = logging.FileHandler('Stocsus.log', 'w')
fh.setLevel(logging.WARNING)
fh.addFilter(SecurityFilter())
formatter = logging.Formatter('%(asctime)s : %(message)s',
                              '%m/%d/%Y %I:%M:%S %p')
fh.setFormatter(formatter)

logger = logging.getLogger('')
logger.propagate = False
logger.addHandler(fh)

# CONFIG
app = Flask(__name__)
# Use your own database for testing
# Connecting to team database will be done towards the end on campus/VM
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@stocsus.cs4jpvtwcnto.eu-west-2.rds.amazonaws.com:3306/stocsus'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Home Page
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
