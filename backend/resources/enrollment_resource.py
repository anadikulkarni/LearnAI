from flask import request
from flask_restful import Resource
from ..models import db, User, Course

class EnrollmentsResource(Resource):
    def post(self):
        data = request.json
        user_id = data.get('user_id')
        course_id = data.get('course_id')

        if not user_id or not course_id:
            return {'message': 'User ID and Course ID are required'}, 400

        user = User.query.get(user_id)
        course = Course.query.get(course_id)

        if not user or not course:
            return {'message': 'User or Course not found'}, 404

        if course in user.courses:
            return {'message': 'User is already enrolled in this course'}, 400

        # Enroll the user in the course
        user.courses.append(course)
        db.session.commit()

        return {'message': f'User {user_id} enrolled in Course {course_id}'}, 201

    # Sample curl command to enroll a user in a course:
    # curl -X POST http://localhost:5000/api/enrollments \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "user_id": 1,
    #            "course_id": 2
    #          }'

    def delete(self):
        data = request.json
        user_id = data.get('user_id')
        course_id = data.get('course_id')

        if not user_id or not course_id:
            return {'message': 'User ID and Course ID are required'}, 400

        user = User.query.get(user_id)
        course = Course.query.get(course_id)

        if not user or not course:
            return {'message': 'User or Course not found'}, 404

        if course not in user.courses:
            return {'message': 'User is not enrolled in this course'}, 404

        # Unenroll the user from the course
        user.courses.remove(course)
        db.session.commit()

        return {'message': f'User {user_id} unenrolled from Course {course_id}'}, 204

    # Sample curl command to unenroll a user from a course:
    # curl -X DELETE http://localhost:5000/api/enrollments \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "user_id": 1,
    #            "course_id": 2
    #          }'

    def get(self, user_id=None, course_id=None):
        if user_id and course_id:
            # Check if the user is enrolled in the course
            user = User.query.get(user_id)
            course = Course.query.get(course_id)

            if not user or not course:
                return {'message': 'User or Course not found'}, 404

            is_enrolled = course in user.courses
            return {'enrolled': is_enrolled}, 200

        elif user_id:
            # Get all courses a user is enrolled in
            user = User.query.get(user_id)
            if not user:
                return {'message': 'User not found'}, 404

            courses = [{'id': course.id, 'title': course.title} for course in user.courses]
            return {'enrolled_courses': courses}, 200

        elif course_id:
            # Get all users enrolled in a course
            course = Course.query.get(course_id)
            if not course:
                return {'message': 'Course not found'}, 404

            users = [{'id': user.id, 'username': user.username} for user in course.users]
            return {'enrolled_users': users}, 200

        else:
            enrollments = db.session.query(User, Course).join(User.courses).all()
            result = [
                {'user_id': user.id, 'username': user.username, 'course_id': course.id, 'course_title': course.title}
                for user, course in enrollments
            ]
            return {'enrollments': result}, 200

    # Sample curl command to get all enrollments:
    # curl -X GET http://localhost:5000/api/enrollments
