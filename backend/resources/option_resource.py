from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..models import db, Option
from ..read_json_fields import option_fields
from flask_security import roles_required

class OptionResource(Resource):
    @marshal_with(option_fields)
    def get(self, option_id=None, question_id=None):
        if option_id:
            option = Option.query.get_or_404(option_id)
            return option
        elif question_id:
            options = Option.query.filter_by(question_id=question_id).all()
            return options
        else:
            options = Option.query.all()
            return options
    # Sample curl command to get all options:
    # curl -X GET http://localhost:5000/api/options
    
    # Sample curl command to get a specific option by ID:
    # curl -X GET http://localhost:5000/api/options/{option_id}

    @marshal_with(option_fields)
    @roles_required('admin', 'instructor')
    def post(self):
        data = request.json
        option = Option(**data)
        db.session.add(option)
        db.session.commit()
        return option, 201
    # Sample curl command to create a new option:
    # curl -X POST http://localhost:5000/api/options \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "content": "Option content",
    #            "is_correct": true,
    #            "question_id": 1
    #          }'

    @marshal_with(option_fields)
    @roles_required('admin', 'instructor')
    def put(self, option_id):
        option = Option.query.get_or_404(option_id)
        data = request.json
        for key, value in data.items():
            setattr(option, key, value)
        db.session.commit()
        return option
    # Sample curl command to update a specific option by ID:
    # curl -X PUT http://localhost:5000/api/options/{option_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "content": "Updated option content",
    #            "is_correct": false,
    #            "question_id": 2
    #          }'

    @roles_required('admin', 'instructor')
    def delete(self, option_id):
        option = Option.query.get_or_404(option_id)
        db.session.delete(option)
        db.session.commit()
        return '', 204
    # Sample curl command to delete a specific option by ID:
    # curl -X DELETE http://localhost:5000/api/options/{option_id}
