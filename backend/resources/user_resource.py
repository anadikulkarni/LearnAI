from flask import jsonify, request
from flask_restful import Resource, marshal
from ..models import db, User, RolesUsers, Role
from ..read_json_fields import user_fields
from werkzeug.security import generate_password_hash
from ..sec import datastore

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id is None:
            users = User.query.all()
            for user in users:
                role_user = RolesUsers.query.filter_by(user_id=user.id).first()
                role = Role.query.get(role_user.role_id) if role_user else None
                user.role_id = role.id if role else None
                user.role_name = role.name if role else None
                user.role_description = role.description if role else None
                user.is_admin = True if role and role.name == 'admin' else False
            return marshal(users, user_fields)  # Using marshal here
        else:
            user = User.query.get_or_404(user_id)
            role_user = RolesUsers.query.filter_by(user_id=user.id).first()
            role = Role.query.get(role_user.role_id) if role_user else None
            user.role_id = role.id if role else None
            user.role_name = role.name if role else None
            user.role_description = role.description if role else None
            user.is_admin = True if role and role.name == 'admin' else False
            return marshal(user, user_fields)  # Using marshal here

    def post(self):
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role_id = data.get('role_id', 3)  # Default role_id to 3 if not provided

        # Validate required fields
        if not username or not email or not password:
            return {'message': 'Username, email, and password are required'}, 400

        # Ensure the role_id is either 3 or 5
        if role_id in [1]:
            return {'message': 'Invalid role_id. Only 3 or 5 are allowed'}, 400

        # Check if user already exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return {'message': 'User with this username or email already exists'}, 400

        # Create user using datastore
        user = datastore.create_user(
            email=email,
            username=username,
            password=generate_password_hash(password),
            active=True,
            roles=[Role.query.get(role_id)]  # Use provided role_id
        )

        # Add user to the local database
        db.session.add(user)
        db.session.commit()

        # Assign role if provided
        role_user = RolesUsers(user_id=user.id, role_id=role_id)
        db.session.add(role_user)
        db.session.commit()

        # Attach role info to user object for marshalling
        role_user = RolesUsers.query.filter_by(user_id=user.id).first()
        role = Role.query.get(role_user.role_id) if role_user else None
        user.role_id = role.id if role else None
        user.role_name = role.name if role else None
        user.role_description = role.description if role else None

        return marshal(user, user_fields), 201  # Using marshal here

    def put(self, user_id):
        data = request.json
        user = User.query.get_or_404(user_id)
        
        # Update user fields
        for key, value in data.items():
            if key == 'role_id':
                # Handle role assignment
                role_id = value
                role_user = RolesUsers.query.filter_by(user_id=user.id).first()
                
                if role_user:
                    role_user.role_id = role_id
                else:
                    role_user = RolesUsers(user_id=user.id, role_id=role_id)
                    db.session.add(role_user)
                
                # Update role details in response
                role = Role.query.get(role_user.role_id)
                user.role_id = role.id
                user.role_name = role.name
                user.role_description = role.description
            else:
                setattr(user, key, value)
        
        db.session.commit()
        
        return marshal(user, user_fields), 200  # Using marshal here

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204
