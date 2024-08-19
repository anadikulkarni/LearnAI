from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..read_json_fields import codingqs_fields
from ..models import Codingqs, db
from flask_security import roles_required
from flask_restful import marshal

class CodingqsResource(Resource):
    @marshal_with(codingqs_fields)
    def get(self, codingqs_id=None, course_id=None):
        if codingqs_id:
            codingqs = Codingqs.query.get_or_404(codingqs_id)
            return codingqs
        elif course_id:
            codingqs_list = Codingqs.query.filter_by(course_id=course_id).all()
            return codingqs_list
        else:
            codingqs_list = Codingqs.query.all()
            return codingqs_list

    # Sample curl command to get all coding questions:
    # curl -X GET http://localhost:5000/api/codingqs

    # Sample curl command to get a specific coding question by ID:
    # curl -X GET http://localhost:5000/api/codingqs/{codingqs_id}

    @marshal_with(codingqs_fields)
    # @roles_required('admin', 'instructor')
    def post(self):
        data = request.json
        codingqs = Codingqs(**data)
        db.session.add(codingqs)
        db.session.commit()
        return codingqs, 201

    # Sample curl command to create a new coding question:
    # curl -X POST http://localhost:5000/api/codingqs \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "title": "New Coding Question",
    #            "description": "Solve this simple problem",
    #            "ex_input": "example input",
    #            "ex_output": "example output",
    #            "course_id": 1
    #          }'

    @marshal_with(codingqs_fields)
    # @roles_required('admin', 'instructor')
    def put(self, codingqs_id):
        codingqs = Codingqs.query.get_or_404(codingqs_id)
        data = request.json
        for key, value in data.items():
            setattr(codingqs, key, value)
        db.session.commit()
        return codingqs

    # Sample curl command to update a specific coding question by ID:
    # curl -X PUT http://localhost:5000/api/codingqs/{codingqs_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "title": "Updated Coding Question Title"
    #          }'

    # @roles_required('admin', 'instructor')
    def delete(self, codingqs_id):
        codingqs = Codingqs.query.get_or_404(codingqs_id)
        db.session.delete(codingqs)
        db.session.commit()
        return '', 204

    # Sample curl command to delete a specific coding question by ID:
    # curl -X DELETE http://localhost:5000/api/codingqs/{codingqs_id}

