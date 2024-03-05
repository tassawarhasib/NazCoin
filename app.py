"""
This is the main application file for the NazCoin project.
It contains the Flask routes and functions for user registration, login, transactions, and more.

The routes in this file include:
- /register: Handles user registration.
- /login: Handles user login.
- /transaction: Handles money transactions between users.
- /buy: Handles buying NazCoin from the bank.
- /logout: Handles user logout.
- /dashboard: Displays user's dashboard with balance and transaction history.
- /index: Displays the index page.
- /aboutUs: Displays the about us page.

The functions in this file include:
- broadcast_transaction: Sends a new transaction to all connected users.
- is_logged_in: Decorator function to check if a user is logged in.
- log_in_user: Logs in a user by updating the session.
- recieve_blockchain: Receives a new transaction from another user.
"""
 
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging # for flask routes
from passlib.hash import sha256_crypt # for password encryption
from flask_mysqldb import MySQL # for mysql database
from functools import wraps # for login decorator
import sys # for command line arguments
from sqlhelpers import * # for mysql database
from forms import * # for forms
import requests # for broadcasting transactions
import time # for timestamp

# initialize the app
app = Flask(__name__) # initialize flask

# configure mysql
app.config['MYSQL_HOST'] = 'localhost' # mysql host
app.config['MYSQL_USER'] = 'root' # mysql username
app.config['MYSQL_PASSWORD'] = '1234' # mysql password
app.config['MYSQL_DB'] = 'crypto' # mysql database
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # mysql cursor class

# initialize mysql
mysql = MySQL(app) # initialize mysql

# wrap to define if the user is currently logged in from session
PORT = sys.argv[1] # get port from command line arguments
connected_users = [{"PORT":5000}, {"PORT":5001}, {"PORT":5002}, {"PORT":5003}, {"PORT":5004}] # list of connected users


def send_email(to_email, subject, body):
    print(to_email)

    api_key = "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"
    sender_email = "nazcoin@nazrasoftware.com"

    # Sendinblue API endpoint
    endpoint = "https://api.sendinblue.com/v3/smtp/email"

    # Sendinblue API request payload
    payload = {
        "sender": {"email": sender_email},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": body,
    }

    # Sendinblue API request headers
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    # Send the email using the requests library
    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code == 201:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")

def broadcast_transaction(data): # broadcast transaction to all connected users
    """
    Broadcasts a transaction to all connected users except the sender.

    Args:
        data (list): List of transactions.

    Returns:
        None
    """
    print("CORRECT")
    print(data)
    for user in connected_users:  # for each connected user
        if str(user['PORT']) != PORT: # if the user is not the sender
            try:
                response = requests.post('http://localhost:{}/recieve_blockchain'.format(user['PORT']),
                                        json={"new_transaction": data[-1]})
                print("Request successful:", response.status_code, response.text)
            except requests.RequestException as e:
                print(f"Error making request: {e}")


def is_logged_in(f): # decorator function to check if a user is logged in
    @wraps(f) # wrap the function
    def wrap(*args, **kwargs): # define the function
        if 'logged_in' in session: # if the user is logged in

            return f(*args, **kwargs) # return the function
        else:
            flash("Unauthorized, please login.", "danger") # flash error message
            return redirect(url_for('login')) # redirect to login page
    return wrap # return the function

# log in the user by updating session


def log_in_user(username): # log in the user by updating session
    users = Table("users", "name", "email", "username", "password")
    user = users.getone("username", username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')

# Registration page


@app.route("/register", methods=['GET', 'POST']) # register route
def register():
    form = RegisterForm(request.form)
    users = Table("users", "name", "email", "username", "password")
    # if form is submitted
    if request.method == 'POST' and form.validate(): # if the form is valid
        # collect form data
        username = form.username.data
        email = form.email.data
        name = form.name.data

        # make sure user does not already exist
        if isnewuser(username): # if the user does not exist
            # add the user to mysql and log them in
            password = sha256_crypt.encrypt(form.password.data) # encrypt the password
            users.insert(name, email, username, password) # insert the user into mysql
            msg = "Hello " + name + ", Thank you for registering on the NazCoin Platform. Kindly se your Username for login."
            send_email(email, "Registration successful", msg)
            log_in_user(username) # log in the user
            return redirect(url_for('dashboard')) # redirect to dashboard
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form) # render the register page 

@app.route("/recieve_blockchain", methods=['POST']) # recieve blockchain route
def recieve_blockchain():

    new_data = (request.json)['new_transaction'] # get the new transaction
    function(new_data) # add the transaction to the blockchain
    return (new_data) # return the new transaction



@app.route("/login", methods=['GET', 'POST'])
def login():
    # if form is submitted
    if request.method == 'POST':
        # collect form data
        username = request.form['username']
        candidate = request.form['password']

        # access users table to get the user's actual password
        users = Table("users", "name", "email", "username", "password")
        user = users.getone("username", username)
        accPass = user.get('password')

        # if the password cannot be found, the user does not exist
        if accPass is None:
            flash("Username is not found", 'danger')
            return redirect(url_for('login'))
        else:
            # verify that the password entered matches the actual password
            if sha256_crypt.verify(candidate, accPass): # if the passwords match
                # log in the user and redirect to Dashboard page
                log_in_user(username)
                flash('You are now logged in.', 'success')
                return redirect(url_for('dashboard'))
            else:
                # if the passwords do not match
                flash("Invalid password", 'danger')
                return redirect(url_for('login'))

    return render_template('login.html')

# Transaction page


@app.route("/transaction", methods=['GET', 'POST']) # transaction route
@is_logged_in
def transaction():
    form = SendMoneyForm(request.form) # get the form
    balance = get_balance(session.get('username')) # get the user's balance
    value = balance * 0.80

    # if form is submitted
    if request.method == 'POST': # if the form is submitted
        amount_data = float(form.amount.data)

        if amount_data * 1.0 > value:
            flash("You can't send more than 80% of your balance.", "danger")
            return redirect(url_for('dashboard'))
        else :
            try:
                send_money(session.get('username'),
                           form.username.data, form.amount.data) # send the money
                broadcast_transaction(dict_blockchain()) # broadcast the transaction
                send_email(session.get('email'), "Nazcoin Sent",
                           "Hello, This is a reminder that you had send " + form.amount.data + " Nazcoin to " + form.username.data)
                try: 
                    remail = get_user_username(form.username.data)
                    send_email(remail, "Nazcoin Received",
                           "Hello, This is a reminder that you had received " + form.amount.data + " Nazcoin from " + session.get('username'))
                    flash("Money Sent!", "success")
                except Exception as e:
                    print(e)
            except Exception as e:
                flash("Transaction Failed!", "danger")
                print("Money Sent Failed!", "danger")
        
        return redirect(url_for('dashboard'))
    
    return render_template('transaction.html', balance=balance, form=form, page='transaction')

# Buy page


@app.route("/buy", methods=['GET', 'POST']) # buy route
@is_logged_in
def buy():
    form = BuyForm(request.form)
    balance = get_balance(session.get('username'))
    if request.method == 'POST':  # if the form is submitted
        # attempt to buy amount
        try:
            send_money("BANK", session.get('username'), form.amount.data)  # send money to the user
            broadcast_transaction(dict_blockchain())
            # broadcast the transaction
            send_email(session.get('email'), "Nazcoin Bought",
                       "Hello, This is a reminder that you had bought " + form.amount.data + " Nazcoin from Bank.")

        except Exception as e:
            print("Purchase UnSuccessful!", "danger")

        flash("Purchase Successful!", "success")
        return redirect(url_for('dashboard'))

    return render_template('buy.html', balance=balance, form=form, page='buy')

# logout the user. Ends current session


@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("Logout success", "success")
    return redirect(url_for('login'))

# Dashboard page


@app.route("/dashboard") # dashboard route
@is_logged_in
def dashboard(): # dashboard function
    balance = get_balance(session.get('username')) # get the user's balance
    blockchain = get_blockchain().chain # get the blockchain
    ct = time.strftime("%I:%M %p") # get the current time
    return render_template('dashboard.html', balance=balance, session=session, ct=ct, blockchain=blockchain, page='dashboard') # render the dashboard page

# Index page


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

# about us


# Run app
if __name__ == '__main__':
    app.secret_key = 'secret123' # set the secret key
    app.run(debug=True, port=PORT) # run the app
