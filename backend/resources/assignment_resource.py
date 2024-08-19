from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..models import db, Assignment
from ..read_json_fields import assignment_fields
from flask_security import roles_required

class AssignmentResource(Resource):
    @marshal_with(assignment_fields)
    def get(self, assignment_id=None):
        if assignment_id is None:
            assignments = Assignment.query.all()
            return assignments
        else:
            assignment = Assignment.query.get_or_404(assignment_id)
            return assignment
    # Sample curl command to get all assignments:
    # curl -X GET http://localhost:5000/api/assignments
    
    # Sample curl command to get a specific assignment by ID:
    # curl -X GET http://localhost:5000/api/assignments/{assignment_id}

    @marshal_with(assignment_fields)
    # @roles_required('admin', 'instructor')
    def post(self):
        data = request.json
        assignment = Assignment(**data)
        db.session.add(assignment)
        db.session.commit()
        return assignment, 201
    # Sample curl command to create a new assignment:
    # curl -X POST http://localhost:5000/api/assignments \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "title": "New Assignment",
    #            "description": "Assignment description",
    #            "due_date": "2024-12-31"
    #          }'

    @marshal_with(assignment_fields)
    # @roles_required('admin', 'instructor')
    def put(self, assignment_id):
        assignment = Assignment.query.get_or_404(assignment_id)
        data = request.json
        for key, value in data.items():
            setattr(assignment, key, value)
        db.session.commit()
        return assignment
    # Sample curl command to update a specific assignment by ID:
    # curl -X PUT http://localhost:5000/api/assignments/{assignment_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "title": "Updated Assignment",
    #            "description": "Updated description",
    #            "due_date": "2025-01-01"
    #          }'

    # @roles_required('admin', 'instructor')
    def delete(self, assignment_id):
        assignment = Assignment.query.get_or_404(assignment_id)
        db.session.delete(assignment)
        db.session.commit()
        return '', 204
    # Sample curl command to delete a specific assignment by ID:
    # curl -X DELETE http://localhost:5000/api/assignments/{assignment_id}
