from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import os
from dotenv import load_dotenv
load_dotenv()

users_bp = Blueprint('users', __name__)


# register user


@users_bp.route("/user/register", methods=["POST"])
def register():
    try:
        from app import mysql
        user_data = request.json
        name = user_data['name']
        email = user_data['email']
        password = user_data['password']
        bio = user_data['bio']
        profile_image = user_data['profile_image']
        DOB = user_data['DOB']

        # checking for email if already exists or not
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, email FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        if user:
            return "user with same email already exists", 409
        else:
            # hashing password
            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt())

            # Execute SQL query to insert user data into the database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (name, email, password, bio, profile_image, DOB) VALUES (%s, %s, %s, %s, %s, %s)",
                        (name, email, hashed_password, bio, profile_image, DOB))
            mysql.connection.commit()
            cur.close()
            return 'User created successfully'

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 'Internal Server Error', 500


# login user
@users_bp.route("/user/login", methods=["POST"])
def login():
    try:
        from app import mysql
        user_data = request.json
        email = user_data['email']
        password = user_data['password']

        # checking for email if already exists or not
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT id, email, password FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        # print(user)
        if user:

            if bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                payload = {
                    'user_id': user[0]
                }
                token = jwt.encode(payload, os.getenv(
                    'JWT_SECRET'), algorithm='HS256')

                return jsonify({'token': token, 'user_id': user[0]})

            return 'Invalid username or password', 401
        else:
            return 'Invalid username or password', 401

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 'Internal Server Error', 500


# {
#     "name" : "Punit",
#     "email":"punit@mail.com",
#     "password":"12345",
#     "bio":"bio1",
#     "profile_image":"https://www.shareicon.net/data/128x128/2016/07/26/802043_man_512x512.png",
#     "DOB":"1998/02/15"
# }
