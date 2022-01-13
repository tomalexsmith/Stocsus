# Stocsus


The global parts' shortage is creating significant challenges for Tharsus as a manufacturer. 
Frequently having to manually search individual websites to check for stock and pricing on components has forced 
productivity to reduce. 
Increasing delays are prolonging product manufacturing timelines at Tharsus.

We have developed a stock checker and price comparison web application that enables employees of Tharsus to quickly 
search a range of websites for a list of parts that are available to satisfy their quantity required, hence eliminating 
the current long and tedious process.


Github Repository: https://github.com/newcastleuniversity-computing/stocsus

## Setting up & Installation
Please install python using the link below if you don't already have it on your system

[Install Python](https://www.python.org/downloads/)


Check python version is 3.10 or above
```bash
python --version
```
Set up virtual environment
```bash
python -m venv stocsus
```
Use package manager to install dependencies
```bash
pip install -r requirements.txt
```
Tell flask where to find your application and set environment variable to development
```bash
set FlASK_APP=app.py
set FLASK_ENV=development
```
## Running the flask application
```bash
python -m flask run
```


