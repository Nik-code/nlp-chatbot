from flask import render_template, request, redirect, session, jsonify
from main import app, db
import re
import bcrypt
import controllers
from security import encrypt_element, decrypt_element
from modules.query_processing import get_response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
def process_query():
    query = request.json['query']
    top5 = request.json['top5']
    response = get_response(query, 'admin')
    if top5:
        return jsonify({'response': response})
    else:
        return jsonify({'response': [response[0]]})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve user information from the form and encrypt them using the public key
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        card_number = request.form['card_number'].replace('-', '')
        password = request.form['password']

        # Regular expression patterns for email and password validation
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        password_regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"

        # Check if email is in the valid format
        if not re.match(email_regex, email):
            return render_template('register.html', alert_message='Invalid email format. Please enter a valid email address.')

        # Check if the password is complex enough
        if not re.match(password_regex, password):
            return render_template('register.html', alert_message='Password does not meet the complexity requirements. It should contain at least one number, one lowercase and one uppercase letter, and be at least 8 characters long.')

        # Check if the card number is valid
        if not card_number.isdigit() or len(card_number) != 16:
            return render_template('register.html', alert_message='Invalid card number. Please enter a valid 16-digit credit/debit card number.')

        # Encrypt the email and card number after validating them
        email = encrypt_element(email)
        card_number = encrypt_element(card_number)

        # Check if the username already exists
        if db.get_user_by_username(username):
            return render_template('register.html', alert_message='Username already exists. Please choose a different username.')

        # Store the user information using the controller
        controllers.insert_user(name, email, username, card_number, password)

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve user information from the form
        username = request.form['username']
        password = request.form['password']

        # Read the user information using the controller
        user_data = controllers.get_user_by_username(username)

        if user_data and bcrypt.checkpw(password.encode(), user_data.password):
            # Store the username in the session for later use
            session['username'] = username
            return redirect('/user')

        # Show a message if the username or password is incorrect
        message = 'Incorrect username or password'
        return render_template('login.html', message=message)

    message = ''
    return render_template('login.html', message=message)


@app.route('/user')
def user():
    # Get the username from the session
    username = session.get('username')

    if username:
        # Fetch the user data using the controller
        user_data = controllers.get_user_by_username(username)
        if user_data:
            email = decrypt_element(user_data.email)
            card_number = decrypt_element(user_data.card_number)
            return render_template('dashboard.html', name=user_data.name, username=user_data.username,
                                   email=email, card_number=card_number)

    return redirect('/login')


@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
