# from flask import Flask, redirect, render_template, request, url_for
# import numpy as np
# import pickle
# import pyrebase
# import tensorflow as tf
# from tensorflow.keras.models import Model
# from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
# from tensorflow.keras.preprocessing.image import load_img, img_to_array
# from keras.utils import pad_sequences
#
# app = Flask(__name__)
# # Add your own Firebase configuration details
# config = {
#     'apiKey': "AIzaSyDM9hliIUZ1a1ukwLlAtQ4BOr1sNuRnULA",
#     'authDomain': "flask-f123e.firebaseapp.com",
#     'projectId': "flask-f123e",
#     'storageBucket': "flask-f123e.appspot.com",
#     'messagingSenderId': "486663157988",
#     'appId': "1:486663157988:web:8dac88b9eb9cb683d2d4f1",
#     'measurementId': "G-1R1H3CW7N1",
#     'databaseURL': "https://flask-f123e-default-rtdb.firebaseio.com/"
# }
#
# # Initialize Firebase
# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()
# db = firebase.database()
#
# # Initialize person as dictionary
# person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}
#
# # Login
# @app.route("/")
# def login():
#     return render_template("login.html")
#
# # Sign up / Register
# @app.route("/signup")
# def signup():
#     return render_template("signup.html")
#
# # Handle login form submission
# @app.route("/result", methods=["POST"])
# def result():
#     if request.method == "POST":
#         result = request.form
#         email = result["email"]
#         password = result["pass"]
#         try:
#             user = auth.sign_in_with_email_and_password(email, password)
#             global person
#             person["is_logged_in"] = True
#             person["email"] = user["email"]
#             person["uid"] = user["localId"]
#             data = db.child("users").get()
#             person["name"] = data.val()[person["uid"]]["name"]
#             return redirect(url_for('index'))
#         except:
#             return redirect(url_for('login'))
#     else:
#         return redirect(url_for('login'))
#
# # Handle signup form submission
# @app.route("/register", methods=["POST"])
# def register():
#     if request.method == "POST":
#         result = request.form
#         email = result["email"]
#         password = result["pass"]
#         name = result["name"]
#         try:
#             auth.create_user_with_email_and_password(email, password)
#             user = auth.sign_in_with_email_and_password(email, password)
#             global person
#             person["is_logged_in"] = True
#             person["email"] = user["email"]
#             person["uid"] = user["localId"]
#             person["name"] = name
#             data = {"name": name, "email": email}
#             db.child("users").child(person["uid"]).set(data)
#             return redirect(url_for('index'))
#         except:
#             return redirect(url_for('signup'))
#     else:
#         return redirect(url_for('signup'))
# # Load MobileNetV2 model
# mobilenet_model = MobileNetV2(weights="imagenet")
# mobilenet_model = Model(inputs=mobilenet_model.inputs, outputs=mobilenet_model.layers[-2].output)
#
# # Load your trained model
# model = tf.keras.models.load_model('mymodel.h5')
#
# # Load the tokenizer
# with open('tokenizer.pkl', 'rb') as tokenizer_file:
#     tokenizer = pickle.load(tokenizer_file)
#
# # Process uploaded image and generate caption
# def generate_caption(image_path, model, tokenizer, max_caption_length):
#     # Load image
#     image = load_img(image_path, target_size=(224, 224))
#     image = img_to_array(image)
#     image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
#     image = preprocess_input(image)
#
#     # Extract features using MobileNetV2
#     image_features = mobilenet_model.predict(image, verbose=0)
#
#     # Define function to get word from index
#     def get_word_from_index(index, tokenizer):
#         return next(
#             (word for word, idx in tokenizer.word_index.items() if idx == index), None
#         )
#
#     # Generate caption using the model
#     caption = "startseq"
#     for _ in range(max_caption_length):
#         sequence = tokenizer.texts_to_sequences([caption])[0]
#         sequence = pad_sequences([sequence], maxlen=max_caption_length)
#         yhat = model.predict([image_features, sequence], verbose=0)
#         predicted_index = np.argmax(yhat)
#         predicted_word = get_word_from_index(predicted_index, tokenizer)
#         caption += " " + predicted_word
#         if predicted_word is None or predicted_word == "endseq":
#             break
#
#     # Remove startseq and endseq
#     generated_caption = caption.replace("startseq", "").replace("endseq", "")
#
#     return generated_caption
#
# @app.route('/index')
# def index():
#     return render_template('index.html')
#
# @app.route('/after', methods=['POST'])
# def after():
#     file = request.files['file1']
#     file.save('static/file.jpg')  # Save the uploaded image
#
#     # Generate caption for the uploaded image
#     generated_caption = generate_caption('static/file.jpg', model, tokenizer, max_caption_length=34)
#
#     return render_template('after.html', image_path='static/file.jpg', generated_caption=generated_caption)
#
# if __name__ == '__main__':
#     app.run(debug=True)
#




from flask import Flask, redirect, render_template, request, url_for, session
import yagmail
import random
import string
import pickle
import numpy as np
import requests
import pyrebase
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from keras.utils import pad_sequences

app = Flask(__name__)
# Add your own Firebase configuration details
config = {
    'apiKey': "AIzaSyDM9hliIUZ1a1ukwLlAtQ4BOr1sNuRnULA",
    'authDomain': "flask-f123e.firebaseapp.com",
    'projectId': "flask-f123e",
    'storageBucket': "flask-f123e.appspot.com",
    'messagingSenderId': "486663157988",
    'appId': "1:486663157988:web:8dac88b9eb9cb683d2d4f1",
    'measurementId': "G-1R1H3CW7N1",
    'databaseURL': "https://flask-f123e-default-rtdb.firebaseio.com/"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app.secret_key = 'mysecret_key'
# Initialize person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

# Sign up / Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/")
def login():
    return render_template("login.html")

# Handle login form submission
@app.route('/result', methods=["POST"])
def result():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['uid'] = user['localId']  # Store UID in session
            session['email'] = email  # Store email in session

            # Check if the logged-in user is an admin
            if email == 'admin1@gmail.com':
                return redirect(url_for('admin_panel'))  # Redirect admin to admin panel
            else:
                return redirect(url_for('index'))  # Redirect regular user to index page

        except Exception as e:
            print("Login Error:", e)  # Print any login errors for debugging
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))

# Admin panel route
@app.route('/admin')
def admin_panel():
    # Fetch all users' data
    users = get_all_users()  # Implement this function to fetch users' data
    return render_template('admin.html', users=users)
#
# # Handle login form submission
# @app.route('/result', methods=["POST"])
# def result():
#     if request.method == "POST":
#         result = request.form
#         email = result["email"]
#         password = result["pass"]
#         try:
#             user = auth.sign_in_with_email_and_password(email, password)
#             session['uid'] = user['localId']  # Store UID in session
#             print(session)  # Print session data for debugging
#             global person
#             person["is_logged_in"] = True
#             person["email"] = user["email"]
#             person["uid"] = user["localId"]
#             data = db.child("users").get()
#             person["name"] = data.val()[person["uid"]]["name"]
#             return redirect(url_for('index'))
#         except Exception as e:
#             print("Login Error:", e)  # Print any login errors for debugging
#             return redirect(url_for('login'))
#     else:
#         return redirect(url_for('login'))


# Add this constant for OTP length
OTP_LENGTH = 6

# Function to generate OTP
def generate_otp():
    otp = ''.join(random.choices(string.digits, k=OTP_LENGTH))
    return otp

# Function to send OTP via email
def send_otp_email(email, otp):
    # Replace 'your_email' and 'your_password' with your actual email credentials
    yag = yagmail.SMTP('deepmachine748@gmail.com', 'prtndxpwmblbfemo')
    yag.send(to=email, subject='OTP Verification', contents=f'Your OTP is: {otp}')

# Route to resend OTP
@app.route('/resend_otp', methods=['POST'])
def resend_otp():
    email = request.form.get('email')
    if email:
        # Generate new OTP
        otp = generate_otp()

        # Expire the old OTP
        session.pop('otp', None)

        # Store new OTP in session
        session['otp'] = otp

        # Send new OTP via email
        send_otp_email(email, otp)

    # Redirect back to the OTP verification page
    return redirect('/verify_otp')

# Modify your registration route to include email domain validation
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        phone = request.form['phone']
        gender = request.form['gender']

        # Check if email contains "@gmail.com"
        if "@gmail.com" not in email:
            return render_template('signup.html', error="Only Gmail addresses are allowed")

        # Check if password and confirm_password match
        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match")

        # Generate OTP
        otp = generate_otp()

        # Send OTP via email
        send_otp_email(email, otp)

        # Store OTP and user data in session
        session['otp'] = otp
        session['name'] = name
        session['email'] = email
        session['password'] = password
        session['phone'] = phone
        session['gender'] = gender

        # Redirect to OTP verification page
        return redirect('/verify_otp')

    return render_template('signup.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        user_otp = request.form['otp']
        stored_otp = session.get('otp')

        if user_otp == stored_otp:
            # If OTP matches, save user data to the database
            name = session.get('name')
            email = session.get('email')
            password = session.get('password')
            phone = session.get('phone')
            gender = session.get('gender')

            try:
                auth.create_user_with_email_and_password(email, password)
                user = auth.sign_in_with_email_and_password(email, password)
                global person
                person["is_logged_in"] = True
                person["email"] = user["email"]
                person["uid"] = user["localId"]
                person["name"] = name

                # Store user profile data in the Firebase Realtime Database
                user_data = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'gender': gender,
                }
                db.child('users').child(person["uid"]).set(user_data)

                return render_template('otp.html', success=True)
            except requests.exceptions.HTTPError as e:
                error_message = e.args[0].response.json()['error']['message']
                if error_message == 'EMAIL_EXISTS':
                    # If email already exists, render the email_registered.html template
                    return render_template('email_registered.html')
                else:
                    # Handle other errors accordingly
                    return render_template('error.html', error_message=error_message)

        else:
            return render_template('otp.html', error='Invalid OTP')

    return render_template('otp.html')

# Load MobileNetV2 model
mobilenet_model = MobileNetV2(weights="imagenet")
mobilenet_model = Model(inputs=mobilenet_model.inputs, outputs=mobilenet_model.layers[-2].output)

# Load your trained model
model = tf.keras.models.load_model('mymodel.h5')

# Load the tokenizer
with open('tokenizer.pkl', 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

# Process uploaded image and generate caption
def generate_caption(image_path, model, tokenizer, max_caption_length):
    # Load image
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)

    # Extract features using MobileNetV2
    image_features = mobilenet_model.predict(image, verbose=0)

    # Define function to get word from index
    def get_word_from_index(index, tokenizer):
        return next(
            (word for word, idx in tokenizer.word_index.items() if idx == index), None
        )

    # Generate caption using the model
    caption = "startseq"
    for _ in range(max_caption_length):
        sequence = tokenizer.texts_to_sequences([caption])[0]
        sequence = pad_sequences([sequence], maxlen=max_caption_length)
        yhat = model.predict([image_features, sequence], verbose=0)
        predicted_index = np.argmax(yhat)
        predicted_word = get_word_from_index(predicted_index, tokenizer)
        caption += " " + predicted_word
        if predicted_word is None or predicted_word == "endseq":
            break

    # Remove startseq and endseq
    generated_caption = caption.replace("startseq", "").replace("endseq", "")

    return generated_caption

def get_all_users():
    users = db.child("users").get().val()
    return users


@app.route('/index')
def index():
    user_data = None  # Initialize user_data with None

    # Check if user is authenticated
    if 'uid' in session:
        uid = session['uid']
        # Fetch user data from Firebase
        user_data = db.child("users").child(uid).get().val()

        print("User Data from Firebase:", user_data)  # Print user data to terminal

    if user_data:
        # Construct person dictionary with user information
        person = {
            'is_logged_in': True,
            'name': user_data.get('name', ''),
            'email': user_data.get('email', ''),
            'phone': user_data.get('phone', ''),
            'gender': user_data.get('gender', '')
        }
    else:
        # If user is not logged in or user data is not available, create a default person dictionary
        person = {'is_logged_in': False}

    # Render the index.html template and pass the person dictionary and user_data
    return render_template('index.html', person=person, user_data=user_data)



@app.route('/after', methods=['POST'])
def after():
    file = request.files['file1']
    file.save('static/file.jpg')  # Save the uploaded image

    # Generate caption for the uploaded image
    generated_caption = generate_caption('static/file.jpg', model, tokenizer, max_caption_length=34)

    return render_template('after.html', image_path='static/file.jpg', generated_caption=generated_caption)

if __name__ == '__main__':
    app.run(debug=True)
