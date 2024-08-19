# This file is now irrelevant as I have refactored login, signup and logout into API endpoints - Azfar.

from flask import current_app as app
from flask_security import auth_required, roles_required
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_security.forms import LoginForm
import requests
from werkzeug.security import check_password_hash
from .sec  import datastore
from .models  import db
from .models import *
from werkzeug.security import generate_password_hash
from flask import  send_from_directory
from datetime import datetime
import os
from flasgger import Swagger, swag_from

@app.get('/')
@swag_from('apidocsmadmusic.yml')
def home():
    """
    Home endpoint.
    ---
    responses:
      200:
        description: Home page
    """
    return render_template('index.html')

@app.get('/admin')
@swag_from('apidocsmadmusic.yml')
@auth_required("token")
@roles_required("admin")
def admin():
    """
    Admin endpoint.
    ---
    responses:
      200:
        description: Welcome admin
    """
    return "Welcome admin"

@app.get('/creator')
@swag_from('apidocsmadmusic.yml')
@auth_required("token")
@roles_required("creator")
def store_manage():
    """
    Creator endpoint.
    ---
    responses:
      200:
        description: Welcome Creator
    """
    return "Welcome Creator"

@app.get('/user')
@swag_from('apidocsmadmusic.yml')
@auth_required("token")
@roles_required("user")
def user():
    """
    User endpoint.
    ---
    responses:
      200:
        description: Welcome User
    """
    return "Welcome User"

@app.post('/user-login')
@swag_from('apidocsmadmusic.yml')
# @cache.cached(timeout=60, key_prefix='user_login')
def user_login():
    """
    User login endpoint.
    ---
    parameters:
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Successful login
      400:
        description: Invalid input
    """
    data = request.get_json()
    email = data.get('email')
    
    # Check cache first
    # cached_result = cache.get(email)
    # if cached_result:
    #     return cached_result
    
    if not email:
        return jsonify({"message": "email not provided"}), 400

    user = datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    if check_password_hash(user.password, data.get("password")):
        # Update last_login
        user.last_login = datetime.now()
        db.session.commit()

        result = jsonify({"token": user.get_auth_token(), "email": user.email, "username":user.username, "role": user.roles[0].name, "user_id": user.id})
        
        # # Cache the result
        # cache.set(email, result, timeout=60)
        
        return result
    else:
        return jsonify({"message": "Wrong Password"}), 400

@app.post('/user-signup')
@swag_from('apidocsmadmusic.yml')
def user_signup():
    """
    User signup endpoint.
    ---
    parameters:
      - name: email
        in: formData
        type: string
        required: true
      - name: username
        in: formData
        type: string
        required: true
      - name: password1
        in: formData
        type: string
        required: true
      - name: password2
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Successful signup
      400:
        description: Invalid input
    """
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password1 = data.get('password1')
    password2 = data.get('password2')

    # Validate required fields
    if not email or not username or not password1 or not password2:
        return jsonify({"message": "All fields are required and must be provided"}), 400

    # Check if the user with the given email already exists
    if datastore.find_user(email=email):
        return jsonify({"message": "User already exists try with a different Email account"}), 409

    # Check if passwords match
    if password1 != password2:
        return jsonify({"message": "Passwords do not match"}), 400

    user_role = datastore.find_or_create_role(name="user")

    user = datastore.find_user(email=email)
    if not user:
      datastore.create_user( username = username, email=email, password=generate_password_hash(password1), active = True, roles=[user_role])
    else:
        return jsonify({"message": "User already exists try with a different Email account"}), 400

    # Commit changes to the database
    db.session.commit()
    return jsonify({"message": "You've signed up successfully! Welcome to Learn AI."}), 200

@app.post('/user-logout')
# @auth_required("token")
@swag_from('apidocsmadmusic.yml')
def user_logout():
    """
    User logout endpoint.
    ---
    responses:
      200:
        description: Successful logout
      401:
        description: User not authenticated
    """

    data = request.get_json()
    email = data.get('email')
    
    # Check cache first
    # cached_result = cache.get(email)
    # if cached_result:
    #     return cached_result
    
    if not email:
        return jsonify({"message": "Already logged out!"}), 400

    user = datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "User not authenticated"}), 401

    # # Clear the authentication token
    # user.auth_token = None
    # db.session.commit()

    return jsonify({"message": "Logged out successfully"}), 200


# Base URL for the external API
genai_api_url = "http://localhost:11434/api/generate"

def call_external_api(payload):
    response = requests.post(genai_api_url, json=payload)
    return response.json()

