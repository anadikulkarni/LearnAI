from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..models import db, CourseRating
from ..read_json_fields import course_rating_fields
from flask_security import roles_required

class CourseRatingResource(Resource):
    @marshal_with(course_rating_fields)
    def get(self, rating_id=None):
        if rating_id is None:
            ratings = CourseRating.query.all()
            return ratings
        else:
            rating = CourseRating.query.get_or_404(rating_id)
            return rating
    # Sample curl command to get all course ratings:
    # curl -X GET http://localhost:5000/api/course_ratings
    
    # Sample curl command to get a specific rating by ID:
    # curl -X GET http://localhost:5000/api/course_ratings/{rating_id}

    @marshal_with(course_rating_fields)
    def post(self):
        data = request.json
        rating = CourseRating(**data)
        db.session.add(rating)
        db.session.commit()
        return rating, 201
    # Sample curl command to create a new course rating:
    # curl -X POST http://localhost:5000/api/course_ratings \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "rating": 4.5,
    #            "comment": "Great course!",
    #            "user_id": 1,
    #            "course_id": 1
    #          }'

    @marshal_with(course_rating_fields)
    def put(self, rating_id):
        rating = CourseRating.query.get_or_404(rating_id)
        data = request.json
        for key, value in data.items():
            setattr(rating, key, value)
        db.session.commit()
        return rating
    # Sample curl command to update a specific course rating by ID:
    # curl -X PUT http://localhost:5000/api/course_ratings/{rating_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "rating": 5.0,
    #            "comment": "Excellent course!",
    #            "user_id": 2,
    #            "course_id": 2
    #          }'

    # @roles_required('admin', 'instructor')
    def delete(self, rating_id):
        rating = CourseRating.query.get_or_404(rating_id)
        db.session.delete(rating)
        db.session.commit()
        return '', 204
    # Sample curl command to delete a specific course rating by ID:
    # curl -X DELETE http://localhost:5000/api/course_ratings/{rating_id}
