from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..models import db, QuizResult
from ..read_json_fields import quiz_result_fields
from flask_security import roles_required

class QuizResultResource(Resource):
    @marshal_with(quiz_result_fields)
    def get(self, result_id=None):
        if result_id is None:
            results = QuizResult.query.all()
            return results
        else:
            result = QuizResult.query.get_or_404(result_id)
            return result
    # Sample curl command to get all quiz results:
    # curl -X GET http://localhost:5000/api/quiz_results
    
    # Sample curl command to get a specific result by ID:
    # curl -X GET http://localhost:5000/api/quiz_results/{result_id}

    @marshal_with(quiz_result_fields)
    @roles_required('admin', 'instructor')
    def post(self):
        data = request.json
        result = QuizResult(**data)
        db.session.add(result)
        db.session.commit()
        return result, 201
    # Sample curl command to create a new quiz result:
    # curl -X POST http://localhost:5000/api/quiz_results \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "score": 95.5,
    #            "user_id": 1,
    #            "quiz_id": 1
    #          }'

    @marshal_with(quiz_result_fields)
    @roles_required('admin', 'instructor')
    def put(self, result_id):
        result = QuizResult.query.get_or_404(result_id)
        data = request.json
        for key, value in data.items():
            setattr(result, key, value)
        db.session.commit()
        return result
    # Sample curl command to update a specific quiz result by ID:
    # curl -X PUT http://localhost:5000/api/quiz_results/{result_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "score": 89.0,
    #            "user_id": 2,
    #            "quiz_id": 2
    #          }'

    @roles_required('admin', 'instructor')
    def delete(self, result_id):
        result = QuizResult.query.get_or_404(result_id)
        db.session.delete(result)
        db.session.commit()
        return '', 204
    # Sample curl command to delete a specific quiz result by ID:
    # curl -X DELETE http://localhost:5000/api/quiz_results/{result_id}
