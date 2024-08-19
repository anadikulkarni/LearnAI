from flask import jsonify, request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import db, User, RolesUsers, Role
from ..sec  import datastore

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')
        role_id = data.get('role_id', 3)

        # Validate required fields
        if not email or not username or not password1 or not password2:
            return {"message": "All fields are required and must be provided"}, 400

        # Check if the user with the given email already exists
        if datastore.find_user(email=email):
            return {"message": "User already exists try with a different Email account"}, 409
        
        if datastore.find_user(username=username):
            return {"message": "Username not available, get creative"}, 409

        # Check if passwords match
        if password1 != password2:
            return {"message": "Passwords do not match"}, 400

        user_role = Role.query.get(role_id)

        user = datastore.find_user(email=email)
        if not user:
            datastore.create_user(
                username=username, 
                email=email, 
                password=generate_password_hash(password1), 
                active=True, 
                roles=[user_role]
            )
            user = datastore.find_user(email=email)
            role_user = RolesUsers(user_id=user.id, role_id=role_id)
            db.session.add(role_user)
        else:
            return {"message": "User already exists try with a different Email account"}, 400

        # Commit changes to the database
        db.session.commit()
        return {"message": "You've signed up successfully! Welcome to Learn AI."}, 200