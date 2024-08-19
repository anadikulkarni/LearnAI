import os
import sys
import json
import time
import pytest
from flask_testing import TestCase
from werkzeug.security import generate_password_hash

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, parent_dir)

print(f"Current directory: {current_dir}")
print(f"Parent directory added to path: {parent_dir}")
print(f"sys.path: {sys.path}")

# Import create_app from app.py
from app import create_app
from backend.models import db
from backend.models import *
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


class TestCourseResource:

    @classmethod
    def setup_class(cls):
        cls.app = create_app(TestingConfig)
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Create a test category
        category = Category(name='Programming')
        db.session.add(category)

        admin_role = Role(name='admin', description='Can create and manage courses')
        db.session.add(admin_role)
        db.session.commit()
        
        # Create a test user with admin role
        admin_user = datastore.create_user(email='admin@email.com', username='admin', password=generate_password_hash('admin'), active=True, roles=[admin_role])
        db.session.add(admin_user)
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


    def test_get_courses(self):
        start_time = time.time()
        response = self.client.get('/api/courses')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
        self.log_test('/api/courses', response, start_time)

    def test_get_course_by_id(self):
        # Create a course first
        start_time = time.time()
        course = Course(title='Python for beginners', description='Test Description', category_id=1, instructor_id=1)
        db.session.add(course)
        db.session.commit()

        response = self.client.get(f'/api/courses/{course.id}')
        assert response.status_code == 200
        assert response.get_json()['title'] == 'Python for beginners'
        self.log_test('/api/courses/1', response, start_time)

    def test_create_course(self):
        start_time = time.time()
        data = {
            'title': 'New Course',
            'description': 'Course description',
            'category_id': 1,
            'instructor_id': 1,
            'youtube_playlist': 'http://youtube.com/playlist'
        }
        response = self.client.post('/api/courses', json=data)
        assert response.status_code == 201
        assert response.get_json()['title'] == 'New Course'
        self.log_test('/api/courses', response, start_time)

    def test_update_course(self):
        start_time = time.time()
        # Create a course first
        course = Course(title='Python for beginners', description='Test Description', category_id=1, instructor_id=1)
        db.session.add(course)
        db.session.commit()

        data = {
            'title': 'Advanced python',
            'description': 'Updated description',
            'category_id': 1,
            'instructor_id': 1,
            'youtube_playlist': 'http://youtube.com/updated-playlist'
        }
        response = self.client.put(f'/api/courses/{course.id}', json=data)
        assert response.status_code == 200
        assert response.get_json()['title'] == 'Advanced python'
        self.log_test('/api/courses/1', response, start_time)

    def test_delete_course(self):
        start_time = time.time()
        # Create a course first
        course = Course(title='Python for beginners', description='Test Description', category_id=1, instructor_id=1)
        db.session.add(course)
        db.session.commit()

        response = self.client.delete(f'/api/courses/{course.id}')
        assert response.status_code == 204
        assert Course.query.get(course.id) is None
        self.log_test('/api/courses', response, start_time)