from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..models import db, Role
from ..read_json_fields import role_fields
from flask_security import roles_required

class RoleResource(Resource):
    @marshal_with(role_fields)
    def get(self, role_id=None):
        if role_id is None:
            roles = Role.query.all()
            return roles
        else:
            role = Role.query.get_or_404(role_id)
            return role
    # Sample curl command to get all roles:
    # curl -X GET http://localhost:5000/api/roles
    
    # Sample curl command to get a specific role by ID:
    # curl -X GET http://localhost:5000/api/roles/{role_id}

    @marshal_with(role_fields)
    @roles_required('admin', 'instructor')
    def post(self):
        data = request.json
        role = Role(**data)
        db.session.add(role)
        db.session.commit()
        return role, 201
    # Sample curl command to create a new role:
    # curl -X POST http://localhost:5000/api/roles \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "name": "Instructor",
    #            "description": "Role for users who are instructors."
    #          }'

    @marshal_with(role_fields)
    @roles_required('admin', 'instructor')
    def put(self, role_id):
        role = Role.query.get_or_404(role_id)
        data = request.json
        for key, value in data.items():
            setattr(role, key, value)
        db.session.commit()
        return role
    # Sample curl command to update a specific role by ID:
    # curl -X PUT http://localhost:5000/api/roles/{role_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "name": "Updated Role",
    #            "description": "Updated description for the role."
    #          }'

    @roles_required('admin', 'instructor')
    def delete(self, role_id):
        role = Role.query.get_or_404(role_id)
        db.session.delete(role)
        db.session.commit()
        return '', 204
    # Sample curl command to delete a specific role by ID:
    # curl -X DELETE http://localhost:5000/api/roles/{role_id}
