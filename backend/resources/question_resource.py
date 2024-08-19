from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..models import db, Question
from ..read_json_fields import question_fields
from flask_security import roles_required
from sqlalchemy.orm import joinedload

class QuestionResource(Resource):
    @marshal_with(question_fields)
    def get(self, question_id=None, quiz_id=None):
        if question_id:
            question = Question.query.options(joinedload(Question.options)).get_or_404(question_id)
            return question
        elif quiz_id:
            questions = Question.query.filter_by(quiz_id=quiz_id).options(joinedload(Question.options)).all()
            return questions
        else:
            questions = Question.query.options(joinedload(Question.options)).all()
            return questions
    # Sample curl command to get all questions:
    # curl -X GET http://localhost:5000/api/questions
    
    # Sample curl command to get a specific question by ID:
    # curl -X GET http://localhost:5000/api/questions/{question_id}

    @marshal_with(question_fields)
    @roles_required('admin', 'instructor')
    def post(self):
        data = request.json
        question = Question(**data)
        db.session.add(question)
        db.session.commit()
        return question, 201
    # Sample curl command to create a new question:
    # curl -X POST http://localhost:5000/api/questions \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "content": "What is the capital of France?",
    #            "quiz_id": 1
    #          }'

    @marshal_with(question_fields)
    @roles_required('admin', 'instructor')
    def put(self, question_id):
        question = Question.query.get_or_404(question_id)
        data = request.json
        for key, value in data.items():
            setattr(question, key, value)
        db.session.commit()
        return question
    # Sample curl command to update a specific question by ID:
    # curl -X PUT http://localhost:5000/api/questions/{question_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "content": "Updated question content",
    #            "quiz_id": 2
    #          }'

    @roles_required('admin', 'instructor')
    def delete(self, question_id):
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return '', 204
    # Sample curl command to delete a specific question by ID:
    # curl -X DELETE http://localhost:5000/api/questions/{question_id}
