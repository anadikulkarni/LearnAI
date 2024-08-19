from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..models import db, AssignmentFeedback
from ..read_json_fields import assignment_feedback_fields
from flask_security import roles_required

class AssignmentFeedbackResource(Resource):
    @marshal_with(assignment_feedback_fields)
    def get(self, assignment_id=None, feedback_id=None):
        if assignment_id is not None:
            # Get feedback for a specific assignment, ordered by created_at in descending order (latest first)
            feedbacks = AssignmentFeedback.query.filter_by(assignment_id=assignment_id).order_by(AssignmentFeedback.created_at.desc()).all()
            return feedbacks
        elif feedback_id is not None:
            # Get a specific feedback by ID
            feedback = AssignmentFeedback.query.get_or_404(feedback_id)
            return feedback
        else:
            # Get all feedback, ordered by created_at in descending order (latest first)
            feedbacks = AssignmentFeedback.query.order_by(AssignmentFeedback.created_at.desc()).all()
            return feedbacks
    # Sample curl command to get all assignment feedback:
    # curl -X GET http://localhost:5000/api/assignment_feedback
    
    # Sample curl command to get a specific feedback by ID:
    # curl -X GET http://localhost:5000/api/assignment_feedback/{feedback_id}

    @marshal_with(assignment_feedback_fields)
    def post(self):
        data = request.json
        feedback = AssignmentFeedback(**data)
        db.session.add(feedback)
        db.session.commit()
        return feedback, 201
    # Sample curl command to create new feedback:
    # curl -X POST http://localhost:5000/api/assignment_feedback \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "feedback": "This is feedback",
    #            "assignment_id": 1
    #          }'

    @marshal_with(assignment_feedback_fields)
    def put(self, feedback_id):
        feedback = AssignmentFeedback.query.get_or_404(feedback_id)
        data = request.json
        for key, value in data.items():
            setattr(feedback, key, value)
        db.session.commit()
        return feedback
    # Sample curl command to update a specific feedback by ID:
    # curl -X PUT http://localhost:5000/api/assignment_feedback/{feedback_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "feedback": "Updated feedback",
    #            "assignment_id": 2
    #          }'

    @roles_required('admin', 'instructor')
    def delete(self, feedback_id):
        feedback = AssignmentFeedback.query.get_or_404(feedback_id)
        db.session.delete(feedback)
        db.session.commit()
        return '', 204
    # Sample curl command to delete a specific feedback by ID:
    # curl -X DELETE http://localhost:5000/api/assignment_feedback/{feedback_id}
