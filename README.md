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
## Using the search page(communicates with Octopart)
Example part number = CFR50J2K2

## Testing the application in the terminal
In order to test the application, enter the below command into the terminal
```bash
pytest
```

## Usage
To utilise the user features use the register function and from there you will be directed to the login page where you 
will
re-enter the details used to register, in order to validate, and after you will arrive at the search page. 
From here you can walk through the application by navigating via the tabs. 

Although, to use the admin functions go to the login tab and use the credentials from models.py in order to gain appropriate access.

