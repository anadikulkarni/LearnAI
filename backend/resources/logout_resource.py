from flask import jsonify, request
from flask_restful import Resource
from ..models import db
from ..sec  import datastore

class LogoutResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        
        # Check cache first
        # cached_result = cache.get(email)
        # if cached_result:
        #     return cached_result
        
        if not email:
            return {"message": "Already logged out!"}, 400

        user = datastore.find_user(email=email)

        if not user:
            return {"message": "User not authenticated"}, 401

        # Clear the authentication token
        # user.auth_token = None
        # db.session.commit()

        return {"message": "Logged out successfully"}, 200
