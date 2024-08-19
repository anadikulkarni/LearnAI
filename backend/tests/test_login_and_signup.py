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
from backend.models import db, Category, Role, User
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

class TestAuthResources:

    @classmethod
    def setup_class(cls):
        cls.app = create_app(TestingConfig)
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        db.create_all()

        # Create roles
        user_role = Role(name='user', description='Regular user')
        db.session.add(user_role)
        db.session.commit()

        # Create a test user
        test_user = datastore.create_user(
            email='testuser@example.com',
            username='testuser',
            password=generate_password_hash('testpassword'),
            active=True,
            roles=[user_role]
        )
        db.session.add(test_user)
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

    # LOGIN TEST CASES
    def test_login_success(self):
        start_time = time.time()
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post('/api/login', json=data)
        assert response.status_code == 200
        assert 'token' in response.get_json()
        self.log_test('/api/login', response, start_time)

    def test_login_missing_email(self):
        start_time = time.time()
        data = {'password': 'testpassword'}
        response = self.client.post('/api/login', json=data)
        assert response.status_code == 400
        assert response.get_json()['message'] == 'email not provided'
        self.log_test('/api/login', response, start_time)

    def test_login_invalid_credentials(self):
        start_time = time.time()
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/login', json=data)
        assert response.status_code == 400
        assert response.get_json()['message'] == 'Wrong Password'
        self.log_test('/api/login', response, start_time)

    # SIGNUP TEST CASES
    def test_signup_success(self):
        start_time = time.time()
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword'
        }
        response = self.client.post('/api/signup', json=data)
        assert response.status_code == 200
        assert response.get_json()['message'] == 'You\'ve signed up successfully! Welcome to Learn AI.'
        self.log_test('/api/signup', response, start_time)

    def test_signup_missing_fields(self):
        start_time = time.time()
        data = {'email': 'newuser@example.com', 'username': 'newuser'}
        response = self.client.post('/api/signup', json=data)
        assert response.status_code == 400
        assert response.get_json()['message'] == 'All fields are required and must be provided'
        self.log_test('/api/signup', response, start_time)

    def test_signup_password_mismatch(self):
        start_time = time.time()
        data = {
            'email': 'newuser2@example.com',
            'username': 'newuser2',
            'password1': 'password1',
            'password2': 'password2'
        }
        response = self.client.post('/api/signup', json=data)
        assert response.status_code == 400
        assert response.get_json()['message'] == 'Passwords do not match'
        self.log_test('/api/signup', response, start_time)

    def test_signup_username_unavailable(self):
        start_time = time.time()
        data = {
            'email': 'testuser5@example.com',
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post('/api/signup', json=data)
        assert response.status_code == 409
        assert response.get_json()['message'] == 'Username not available, get creative'
        self.log_test('/api/signup', response, start_time)

    # LOGOUT TEST CASES
    def test_logout_success(self):
        start_time = time.time()
        data = {'email': 'testuser@example.com'}
        response = self.client.post('/api/logout', json=data)
        assert response.status_code == 200
        assert response.get_json()['message'] == 'Logged out successfully'
        self.log_test('/api/logout', response, start_time)

    def test_logout_missing_email(self):
        start_time = time.time()
        response = self.client.post('/api/logout', json={})
        assert response.status_code == 400
        assert response.get_json()['message'] == 'Already logged out!'
        self.log_test('/api/logout', response, start_time)

    def test_logout_user_not_authenticated(self):
        start_time = time.time()
        data = {'email': 'nonexistentuser@example.com'}
        response = self.client.post('/api/logout', json=data)
        assert response.status_code == 401
        assert response.get_json()['message'] == 'User not authenticated'
        self.log_test('/api/logout', response, start_time)
