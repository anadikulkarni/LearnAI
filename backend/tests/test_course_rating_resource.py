import os
import sys
import json
import time
import pytest
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, parent_dir)

print(f"Current directory: {current_dir}")
print(f"Parent directory added to path: {parent_dir}")
print(f"sys.path: {sys.path}")

# Import create_app from app.py
from app import create_app
from backend.models import db, CourseRating, User, Course, Role
from backend.sec import datastore
from config import TestingConfig

# Define the path for the Results JSON file
RESULTS_FILE = 'test_results.json'

def load_results():
    """Load existing results from the JSON file."""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_results(results):
    """Save results to the JSON file."""
    with open(RESULTS_FILE, 'w') as file:
        json.dump(results, file, indent=4)
    print(f"Data saved to {RESULTS_FILE}")


class TestCourseRatingResource:

    @classmethod
    def setup_class(cls):
        cls.app = create_app(TestingConfig)
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        db.create_all()

        # Create test roles
        admin_role = Role(name='admin', description='Can create and manage courses')
        instructor_role = Role(name='instructor', description='Can instruct courses')
        db.session.add(admin_role)
        db.session.add(instructor_role)
        db.session.commit()
        
        # Create test users
        admin_user = datastore.create_user(email='admin@example.com', username='admin', password=generate_password_hash('admin'), active=True, roles=[admin_role])
        instructor_user = datastore.create_user(email='instructor@example.com', username='instructor', password=generate_password_hash('instructor'), active=True, roles=[instructor_role])
        db.session.add(admin_user)
        db.session.add(instructor_user)
        db.session.commit()
        
        # Create a test course
        course = Course(title='PDSA 101', description='Test Description', category_id=1, instructor_id=instructor_user.id)
        db.session.add(course)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
    
    def log_test(self, endpoint, response, start_time):
        """Log test details to a JSON file."""
        elapsed_time = time.time() - start_time
        results = load_results()
        result = {
            'endpoint': endpoint,
            'request_url': response.request.url,
            'response_status': response.status_code,
            'response_data': response.data.decode('utf-8'),
            'time_taken': round(elapsed_time, 2)
        }
        results.append(result)
        save_results(results)


    def test_get_course_ratings(self):
        start_time = time.time()
        response = self.client.get('/api/course_ratings')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
        self.log_test('/api/course_ratings', response, start_time)

    def test_get_course_rating_by_id(self):
        # Create a course rating first
        start_time = time.time()
        rating = CourseRating(rating=4.5, comment="Great course!", user_id=1, course_id=1)
        db.session.add(rating)
        db.session.commit()

        response = self.client.get(f'/api/course_ratings/{rating.id}')
        assert response.status_code == 200
        assert response.get_json()['rating'] == 4.5
        self.log_test(f'/api/course_ratings/{rating.id}', response, start_time)

    def test_post_course_rating(self):
        start_time = time.time()
        data = {
            "rating": 4.5,
            "comment": "Great course!",
            "user_id": 1,
            "course_id": 1
        }
        response = self.client.post('/api/course_ratings', json=data)
        assert response.status_code == 201
        assert response.get_json()['rating'] == 4.5
        self.log_test('/api/course_ratings', response, start_time)

    def test_put_course_rating(self):
        # Create a course rating first
        start_time = time.time()
        rating = CourseRating(rating=4.5, comment="Great course!", user_id=1, course_id=1)
        db.session.add(rating)
        db.session.commit()

        data = {
            "rating": 5.0,
            "comment": "Excellent course!",
            "user_id": 1,
            "course_id": 1
        }
        response = self.client.put(f'/api/course_ratings/{rating.id}', json=data)
        assert response.status_code == 200
        assert response.get_json()['rating'] == 5.0
        self.log_test(f'/api/course_ratings/{rating.id}', response, start_time)

    def test_delete_course_rating(self):
        # Create a course rating first
        start_time = time.time()
        rating = CourseRating(rating=4.5, comment="Great course!", user_id=1, course_id=1)
        db.session.add(rating)
        db.session.commit()

        response = self.client.delete(f'/api/course_ratings/{rating.id}')
        assert response.status_code == 204
        self.log_test(f'/api/course_ratings/{rating.id}', response, start_time)
