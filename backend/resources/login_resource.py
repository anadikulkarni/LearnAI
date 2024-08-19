from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..read_json_fields import user_fields
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from ..models import db
from ..sec import datastore

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        
        # Check cache first
        # cached_result = cache.get(email)
        # if cached_result:
        #     return cached_result
        
        if not email:
            return {"message": "email not provided"}, 400

        user = datastore.find_user(email=email)

        if not user:
            return {"message": "User Not Found"}, 404

        if check_password_hash(user.password, data.get("password")):
            # Update last_login
            user.last_login = datetime.now()
            db.session.commit()

            result = {
                "token": user.get_auth_token(), 
                "email": user.email, 
                "username": user.username, 
                "role": user.roles[0].name, 
                "user_id": user.id
            }
            
            # Cache the result
            # cache.set(email, result, timeout=60)
            
            return result, 200
        else:
            return {"message": "Wrong Password"}, 400
