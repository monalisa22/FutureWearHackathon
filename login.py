import numpy as np
from flask import Flask, redirect, url_for, request, jsonify, render_template, session, flash
import uuid as uuid
from firebase import firebase


app = Flask(__name__)
app.secret_key = "hello"
firebase = firebase.FirebaseApplication('https://titanesp32-default-rtdb.asia-southeast1.firebasedatabase.app/', None)
app.app_context().push()

@app.route('/')
def home():
    return render_template('dashboard.html')
@app.route('/home')
def homei():
    return render_template('dashboard.html')

@app.route("/login_page")
def login_page():
    return render_template("login.html")

# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    result = firebase.get('/new_test', None)
    username = request.form["Username"]
     # Convert dict_values to a list of dictionaries
    user_list = list(result.values())

    # Check if the provided username exists in any dictionary
    for user_data in user_list:
        if "username" in user_data and user_data["username"] == username:
            return redirect(url_for('dashboard'))

    # If username doesn't exist in any dictionary, show flash message and render login template
    flash("That User Doesn't Exist! Try Again...")
    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard2.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    return render_template('index.html')

# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
def logout():
	flash("You Have Been Logged Out!  Thanks For Stopping By...")
	return redirect(url_for('home'))


@app.route('/signin', methods=["GET", "POST"])
def signin():
    if request.method == 'POST' and len(dict(request.form)) > 0:
        userdata = dict(request.form)
        username = userdata["username"]
        email = userdata["email"]
        name = userdata["name"]
        age = userdata["age"]
        gender = userdata["gender"]
        height = userdata["height"]
        weight = userdata["weight"]
        sleep_duration = userdata["sleep_duration"]
        
        result = firebase.get('/new_test', None)
        # username = request.form["Username"]
         # Convert dict_values to a list of dictionaries
        user_list = list(result.values())

        # Check if the provided username exists in any dictionary
        for user_data in user_list:
            if "username" in user_data and user_data["username"] == username:
                flash("That Username Already Exits!")
                return render_template('login.html')

        
        new_data = {"username": username,"email": email,"name": name, "age": age,"gender": gender,"height": height,"weight": weight,"sleep_duration": sleep_duration}
        firebase.post("/new_test", new_data)
        return render_template('login.html',prediction_text=username)
    
    else:
        if "user" in session:
            flash("Already Logged In!")
            return render_template('login.html')
   

if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)