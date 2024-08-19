# backend/resources/quiz_resource.py

from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..models import QuizResult, db, Quiz, Question, Option
from ..read_json_fields import quiz_fields, quiz_result_fields
from flask_security import roles_required
from flask_restful import Resource, marshal

class QuizResource(Resource):
    @marshal_with(quiz_fields)
    def get(self, quiz_id=None, course_id=None):
        if quiz_id:
            quiz = Quiz.query.options(
                db.subqueryload(Quiz.questions).subqueryload(Question.options)
            ).get_or_404(quiz_id)
            return quiz
        elif course_id:
            quizzes = Quiz.query.filter_by(course_id=course_id).options(
                db.subqueryload(Quiz.questions).subqueryload(Question.options)
            ).all()
            return quizzes
        else:
            quizzes = Quiz.query.options(
                db.subqueryload(Quiz.questions).subqueryload(Question.options)
            ).all()
            return quizzes


    # Sample curl command to get all quizzes:
    # curl -X GET http://localhost:5000/api/quizzes
    
    # Sample curl command to get a specific quiz by ID:
    # curl -X GET http://localhost:5000/api/quizzes/{quiz_id}

    @marshal_with(quiz_fields)
    def post(self):
        data = request.json
        quiz = Quiz(**data)
        db.session.add(quiz)
        db.session.commit()
        return quiz, 201

    # Sample curl command to create a new quiz:
    # curl -X POST http://localhost:5000/api/quizzes \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "title": "New Quiz"
    #          }'

    @marshal_with(quiz_fields)
    @roles_required('admin', 'instructor')
    def put(self, quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        data = request.json
        for key, value in data.items():
            setattr(quiz, key, value)
        db.session.commit()
        return quiz

    # Sample curl command to update a specific quiz by ID:
    # curl -X PUT http://localhost:5000/api/quizzes/{quiz_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "title": "Updated Quiz Title"
    #          }'

    @roles_required('admin', 'instructor')
    def delete(self, quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        db.session.delete(quiz)
        db.session.commit()
        return '', 204

    # Sample curl command to delete a specific quiz by ID:
    # curl -X DELETE http://localhost:5000/api/quizzes/{quiz_id}



class SubmitQuizResource(Resource):
    def post(self, quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        data = request.json


        answers = data.get('answers')

        if not answers:
            return {'message': 'Answers are required'}, 400

        total_questions = len(quiz.questions)
        correct_answers = 0

        for question in quiz.questions:
            selected_option_id = answers.get(str(question.id))
            if selected_option_id:
                selected_option = Option.query.get(selected_option_id)
                if selected_option and selected_option.is_correct:
                    correct_answers += 1

        # Calculate the score as a percentage
        score = (correct_answers / total_questions) * 100

        # Create a new QuizResult object
        quiz_result = QuizResult(
            score=score,
            user_id=3,  # Assuming you're using Flask-Security for authentication
            quiz_id=quiz.id
        )

        # Save the quiz result to the database
        db.session.add(quiz_result)
        db.session.commit()
        return marshal(quiz_result, quiz_result_fields), 201

    # Sample curl command to submit a quiz and get the result:
    # curl -X POST http://localhost:5000/api/submit_quiz/{quiz_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "answers": {
    #              "1": 2,
    #              "2": 5,
    #              "3": 9
    #            }
    #          }'
